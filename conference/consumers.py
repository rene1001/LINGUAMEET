import json
import base64
import asyncio
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Room, Participant, ConversationHistory
from django.conf import settings
import logging

# Choisir le pipeline audio selon la configuration
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Détecter le meilleur pipeline disponible
USE_FREE_PREMIUM = os.getenv('USE_FREE_PREMIUM', 'False').lower() == 'true'
USE_GOOGLE_CLOUD = getattr(settings, 'USE_GOOGLE_CLOUD_AUDIO', False)

if USE_FREE_PREMIUM:
    # Pipeline Google STT + Gemini + Google TTS
    try:
        from .ai_pipeline_free_premium import FreePremiumAudioProcessor as AudioProcessor
        logger.info("🎓 Pipeline Google + Gemini activé (STT + Traduction + TTS)")
    except ImportError as e:
        logger.warning(f"⚠️ Pipeline Google + Gemini non disponible: {e}")
        from .ai_pipeline import AudioProcessor
        logger.info("📦 Fallback vers pipeline standard (Vosk/gTTS)")
elif USE_GOOGLE_CLOUD:
    # Pipeline Google Cloud complet
    try:
        from .ai_pipeline_google_cloud import GoogleCloudAudioProcessor as AudioProcessor
        logger.info("🚀 Pipeline Google Cloud complet activé")
    except ImportError:
        from .ai_pipeline import AudioProcessor
        logger.warning("⚠️ Google Cloud non disponible, fallback vers Vosk/gTTS")
else:
    # Pipeline standard (Vosk + googletrans + gTTS)
    from .ai_pipeline import AudioProcessor
    logger.info("📦 Pipeline audio standard (Vosk/gTTS)")

class ConferenceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.participant_id = None
        self.room_group_name = None
        self.audio_processor = AudioProcessor()

    async def connect(self):
        """Gérer la connexion WebSocket"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'conference_{self.room_id}'

        # Vérifier que la salle existe
        room = await self.get_room()
        if not room:
            await self.close()
            return

        # Rejoindre le groupe de la salle
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket connecté pour la salle {self.room_id}")

    async def disconnect(self, close_code):
        """Gérer la déconnexion WebSocket"""
        if self.room_group_name:
            # Quitter le groupe
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            # Marquer le participant comme inactif
            if self.participant_id:
                await self.mark_participant_inactive()

        logger.info(f"WebSocket déconnecté de la salle {self.room_id}")

    async def receive(self, text_data):
        """Recevoir des messages du client"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'join':
                await self.handle_join(data)
            elif message_type == 'audio_data':
                await self.handle_audio_data(data)
            elif message_type == 'microphone_toggle':
                await self.handle_microphone_toggle(data)
            elif message_type == 'video_toggle':
                await self.handle_video_toggle(data)
            elif message_type == 'webrtc_offer':
                await self.handle_webrtc_offer(data)
            elif message_type == 'webrtc_answer':
                await self.handle_webrtc_answer(data)
            elif message_type == 'webrtc_ice_candidate':
                await self.handle_webrtc_ice_candidate(data)
            else:
                logger.warning(f"Type de message non reconnu: {message_type}")

        except json.JSONDecodeError:
            logger.error("Erreur décodage JSON")
        except Exception as e:
            logger.error(f"Erreur traitement message: {e}")

    async def handle_join(self, data):
        """Gérer l'arrivée d'un participant"""
        participant_id = data.get('participant_id')
        name = data.get('name')
        language = data.get('language')
        reception_language = data.get('reception_language')

        # Mettre à jour le participant
        await self.update_participant_info(
            participant_id, name, language, reception_language
        )

        self.participant_id = participant_id

        # Notifier les autres participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_joined',
                'participant_id': participant_id,
                'name': name,
                'language': language,
                'reception_language': reception_language
            }
        )

        # Envoyer la liste des participants existants
        participants = await self.get_room_participants()
        await self.send(text_data=json.dumps({
            'type': 'participants_list',
            'participants': participants
        }))

    async def handle_audio_data(self, data):
        """Traiter les données audio reçues"""
        if not self.participant_id:
            return

        audio_base64 = data.get('audio_data')
        if not audio_base64:
            return

        try:
            # Décoder l'audio base64
            audio_bytes = base64.b64decode(audio_base64)

            # Traiter l'audio (transcription, traduction, synthèse)
            result = await self.process_audio_pipeline(
                audio_bytes, 
                self.participant_id
            )

            if result:
                # Envoyer l'audio traduit à tous les participants
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'audio_translated',
                        'participant_id': self.participant_id,
                        'participant_name': result['participant_name'],
                        'original_text': result['original_text'],
                        'translated_text': result['translated_text'],
                        'audio_data': result['audio_base64'],
                        'target_language': result['target_language']
                    }
                )

                # Envoyer la dernière transcription à l'émetteur (lui-même)
                await self.send(text_data=json.dumps({
                    'type': 'last_transcription',
                    'who': 'me',
                    'original_text': result['original_text'],
                    'translated_text': result['translated_text'],
                    'original_language': result['original_language'],
                    'target_language': result['target_language']
                }))

                # Envoyer la dernière transcription à tous les autres participants
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'last_transcription_broadcast',
                        'who': 'other',
                        'participant_id': self.participant_id,
                        'original_text': result['original_text'],
                        'translated_text': result['translated_text'],
                        'original_language': result['original_language'],
                        'target_language': result['target_language']
                    }
                )

                # Sauvegarder la conversation pour chaque participant
                await self.save_conversation_for_all_participants(result)

        except Exception as e:
            logger.error(f"Erreur traitement audio: {e}")

    async def handle_microphone_toggle(self, data):
        """Gérer l'activation/désactivation du microphone"""
        active = data.get('active', False)
        
        await self.update_participant_microphone(self.participant_id, active)

        # Notifier les autres participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_update',
                'participant_id': self.participant_id,
                'updates': {
                    'microphone_active': active
                }
            }
        )

    async def handle_video_toggle(self, data):
        """Gérer l'activation/désactivation de la vidéo"""
        active = data.get('active', False)
        
        await self.update_participant_video(self.participant_id, active)

        # Notifier les autres participants
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_update',
                'participant_id': self.participant_id,
                'updates': {
                    'video_active': active
                }
            }
        )

    async def handle_webrtc_offer(self, data):
        """Gérer une offre WebRTC pour la vidéo"""
        target_id = data.get('target_id')
        offer = data.get('offer')
        
        if target_id and offer:
            # Envoyer l'offre au participant cible
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer_forward',
                    'from_id': self.participant_id,
                    'target_id': target_id,
                    'offer': offer
                }
            )

    async def handle_webrtc_answer(self, data):
        """Gérer une réponse WebRTC"""
        target_id = data.get('target_id')
        answer = data.get('answer')
        
        if target_id and answer:
            # Envoyer la réponse au participant cible
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer_forward',
                    'from_id': self.participant_id,
                    'target_id': target_id,
                    'answer': answer
                }
            )

    async def handle_webrtc_ice_candidate(self, data):
        """Gérer un candidat ICE WebRTC"""
        target_id = data.get('target_id')
        candidate = data.get('candidate')
        
        if target_id and candidate:
            # Envoyer le candidat au participant cible
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_ice_candidate_forward',
                    'from_id': self.participant_id,
                    'target_id': target_id,
                    'candidate': candidate
                }
            )

    async def process_audio_pipeline(self, audio_bytes, participant_id):
        """Pipeline complet de traitement audio"""
        try:
            # Obtenir les informations du participant
            participant = await self.get_participant(participant_id)
            if not participant:
                return None

            # Étape 1: Transcription (speech-to-text)
            original_text = await self.audio_processor.speech_to_text(audio_bytes)
            if not original_text:
                return None

            # Étape 2: Traduction
            translated_text = await self.audio_processor.translate(
                original_text, 
                participant.langue_parole, 
                participant.langue_souhaitée
            )

            # Étape 3: Synthèse vocale (text-to-speech)
            translated_audio = await self.audio_processor.text_to_speech(
                translated_text, 
                participant.langue_souhaitée
            )

            # Encoder l'audio en base64
            audio_base64 = base64.b64encode(translated_audio).decode('utf-8')

            return {
                'participant_name': participant.nom,
                'original_text': original_text,
                'translated_text': translated_text,
                'audio_base64': audio_base64,
                'target_language': participant.langue_souhaitée,
                'original_language': participant.langue_parole,
                'audio_bytes': translated_audio,
                'speaker_id': participant_id
            }

        except Exception as e:
            logger.error(f"Erreur pipeline audio: {e}")
            return None

    async def save_conversation_for_all_participants(self, result):
        """Sauvegarder la conversation pour tous les participants"""
        try:
            # Obtenir tous les participants actifs dans la salle
            participants = await self.get_all_room_participants()
            
            for participant in participants:
                # Ne pas sauvegarder pour l'émetteur lui-même
                if str(participant['id']) == result['speaker_id']:
                    continue
                
                # Sauvegarder la conversation pour ce participant
                await self.save_conversation_record(
                    speaker_id=result['speaker_id'],
                    listener_id=participant['id'],
                    original_text=result['original_text'],
                    translated_text=result['translated_text'],
                    original_language=result['original_language'],
                    target_language=participant['reception_language'],
                    audio_bytes=result['audio_bytes']
                )
                
        except Exception as e:
            logger.error(f"Erreur sauvegarde conversation: {e}")

    async def save_conversation_record(self, speaker_id, listener_id, original_text, 
                                     translated_text, original_language, target_language, audio_bytes):
        """Sauvegarder un enregistrement de conversation"""
        try:
            # Créer l'enregistrement de conversation
            conversation = await self.create_conversation_record(
                speaker_id=speaker_id,
                listener_id=listener_id,
                original_text=original_text,
                translated_text=translated_text,
                original_language=original_language,
                target_language=target_language,
                audio_bytes=audio_bytes
            )
            
            logger.info(f"Conversation sauvegardée: {conversation.id}")
            
        except Exception as e:
            logger.error(f"Erreur création enregistrement conversation: {e}")

    # Méthodes de groupe pour envoyer des messages
    async def participant_joined(self, event):
        """Envoyer l'information qu'un participant a rejoint"""
        await self.send(text_data=json.dumps({
            'type': 'participant_joined',
            'participant_id': event['participant_id'],
            'name': event['name'],
            'language': event['language'],
            'reception_language': event['reception_language']
        }))

    async def participant_left(self, event):
        """Envoyer l'information qu'un participant a quitté"""
        await self.send(text_data=json.dumps({
            'type': 'participant_left',
            'participant_id': event['participant_id'],
            'name': event['name']
        }))

    async def audio_translated(self, event):
        """Envoyer l'audio traduit"""
        await self.send(text_data=json.dumps({
            'type': 'audio_translated',
            'participant_id': event['participant_id'],
            'participant_name': event['participant_name'],
            'original_text': event['original_text'],
            'translated_text': event['translated_text'],
            'audio_data': event['audio_data'],
            'target_language': event['target_language']
        }))

    async def participant_update(self, event):
        """Envoyer les mises à jour de participant"""
        await self.send(text_data=json.dumps({
            'type': 'participant_update',
            'participant_id': event['participant_id'],
            'updates': event['updates']
        }))

    async def webrtc_offer_forward(self, event):
        """Transférer une offre WebRTC au participant cible"""
        if str(self.participant_id) == str(event['target_id']):
            await self.send(text_data=json.dumps({
                'type': 'webrtc_offer',
                'from_id': event['from_id'],
                'offer': event['offer']
            }))

    async def webrtc_answer_forward(self, event):
        """Transférer une réponse WebRTC au participant cible"""
        if str(self.participant_id) == str(event['target_id']):
            await self.send(text_data=json.dumps({
                'type': 'webrtc_answer',
                'from_id': event['from_id'],
                'answer': event['answer']
            }))

    async def webrtc_ice_candidate_forward(self, event):
        """Transférer un candidat ICE au participant cible"""
        if str(self.participant_id) == str(event['target_id']):
            await self.send(text_data=json.dumps({
                'type': 'webrtc_ice_candidate',
                'from_id': event['from_id'],
                'candidate': event['candidate']
            }))

    async def last_transcription_broadcast(self, event):
        # Ne pas renvoyer à l'émetteur
        if str(self.participant_id) == str(event.get('participant_id')):
            return
        await self.send(text_data=json.dumps({
            'type': 'last_transcription',
            'who': 'other',
            'original_text': event['original_text'],
            'translated_text': event['translated_text'],
            'original_language': event['original_language'],
            'target_language': event['target_language']
        }))

    # Méthodes de base de données
    @database_sync_to_async
    def get_room(self):
        """Obtenir la salle depuis la base de données"""
        try:
            return Room.objects.get(id=self.room_id, actif=True)
        except (ObjectDoesNotExist, ValueError, ValidationError):
            return None

    @database_sync_to_async
    def get_participant(self, participant_id):
        """Obtenir un participant depuis la base de données"""
        try:
            return Participant.objects.get(id=participant_id, actif=True)
        except (ObjectDoesNotExist, ValueError, ValidationError):
            return None

    @database_sync_to_async
    def update_participant_info(self, participant_id, name, language, reception_language):
        """Mettre à jour les informations d'un participant"""
        try:
            participant = Participant.objects.get(id=participant_id)
            participant.socket_id = self.channel_name
            participant.langue_parole = language
            participant.langue_souhaitée = reception_language
            participant.save()
        except (ObjectDoesNotExist, ValueError, ValidationError):
            pass

    @database_sync_to_async
    def update_participant_microphone(self, participant_id, active):
        """Mettre à jour l'état du microphone d'un participant"""
        try:
            participant = Participant.objects.get(id=participant_id)
            participant.micro_actif = active
            participant.save()
        except (ObjectDoesNotExist, ValueError, ValidationError):
            pass

    @database_sync_to_async
    def update_participant_video(self, participant_id, active):
        """Mettre à jour l'état de la vidéo d'un participant"""
        try:
            participant = Participant.objects.get(id=participant_id)
            participant.video_actif = active
            participant.save()
        except (ObjectDoesNotExist, ValueError, ValidationError):
            pass

    @database_sync_to_async
    def mark_participant_inactive(self):
        """Marquer un participant comme inactif"""
        try:
            participant = Participant.objects.get(id=self.participant_id)
            participant.actif = False
            participant.save()
        except (ObjectDoesNotExist, ValueError, ValidationError):
            pass

    @database_sync_to_async
    def get_room_participants(self):
        """Obtenir la liste des participants actifs dans la salle"""
        participants = Participant.objects.filter(
            room_id=self.room_id, 
            actif=True
        ).exclude(id=self.participant_id)
        
        return [
            {
                'id': str(p.id),
                'name': p.nom,
                'language': p.langue_parole,
                'reception_language': p.langue_souhaitée,
                'microphone_active': p.micro_actif,
                'video_active': p.video_actif
            }
            for p in participants
        ]

    @database_sync_to_async
    def get_all_room_participants(self):
        """Obtenir tous les participants actifs dans la salle"""
        participants = Participant.objects.filter(
            room_id=self.room_id, 
            actif=True
        )
        
        return [
            {
                'id': str(p.id),
                'name': p.nom,
                'language': p.langue_parole,
                'reception_language': p.langue_souhaitée,
                'microphone_active': p.micro_actif,
                'video_active': p.video_actif
            }
            for p in participants
        ]

    @database_sync_to_async
    def create_conversation_record(self, speaker_id, listener_id, original_text, 
                                 translated_text, original_language, target_language, audio_bytes):
        """Créer un enregistrement de conversation avec fichier audio"""
        try:
            # Obtenir les objets
            speaker = Participant.objects.get(id=speaker_id)
            listener = Participant.objects.get(id=listener_id)
            room = Room.objects.get(id=self.room_id)
            
            # Créer l'enregistrement de conversation
            conversation = ConversationHistory.objects.create(
                room=room,
                speaker=speaker,
                listener=listener,
                original_text=original_text,
                translated_text=translated_text,
                original_language=original_language,
                target_language=target_language,
                audio_duration=len(audio_bytes) / 16000  # Estimation basée sur 16kHz
            )
            
            # Sauvegarder le fichier audio
            if audio_bytes:
                # Créer le nom de fichier
                filename = f"conversation_{conversation.id}_{speaker.nom}_{listener.nom}.wav"
                
                # Sauvegarder le fichier
                conversation.audio_file.save(
                    filename,
                    ContentFile(audio_bytes),
                    save=True
                )
            
            return conversation
            
        except Exception as e:
            logger.error(f"Erreur création conversation: {e}")
            return None 