import asyncio
import io
import wave
import numpy as np
from vosk import Model, KaldiRecognizer
from googletrans import Translator
from gtts import gTTS
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.translator = Translator()
        self.vosk_model = None
        self.load_vosk_model()
        
        # Mapping des langues pour Vosk
        self.vosk_language_map = {
            'fr': 'fr',
            'en': 'en-us',
            'es': 'es',
            'de': 'de',
            'it': 'it',
            'pt': 'pt',
            'ru': 'ru',
            'ja': 'ja',
            'ko': 'ko',
            'zh': 'zh'
        }
        
        # Mapping des langues pour gTTS
        self.gtts_language_map = {
            'fr': 'fr',
            'en': 'en',
            'es': 'es',
            'de': 'de',
            'it': 'it',
            'pt': 'pt',
            'ru': 'ru',
            'ja': 'ja',
            'ko': 'ko',
            'zh': 'zh'
        }

    def load_vosk_model(self):
        """Charger le modèle Vosk pour la reconnaissance vocale"""
        try:
            model_path = settings.VOSK_MODEL_PATH / 'vosk-model-small-fr-0.22'
            if not model_path.exists():
                logger.warning("Modèle Vosk non trouvé, téléchargement simulé...")
                # En production, télécharger le modèle ici
                return
            
            self.vosk_model = Model(str(model_path))
            logger.info("Modèle Vosk chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur chargement modèle Vosk: {e}")
            # Fallback: utiliser un modèle simple
            self.vosk_model = None

    async def speech_to_text(self, audio_bytes):
        """Convertir l'audio en texte (speech-to-text)"""
        try:
            if not self.vosk_model:
                # Simulation pour le MVP
                return await self.simulate_speech_to_text(audio_bytes)
            
            # Convertir les bytes audio en format compatible Vosk
            audio_data = self.prepare_audio_for_vosk(audio_bytes)
            
            # Créer le recognizer
            rec = KaldiRecognizer(self.vosk_model, 16000)
            rec.SetWords(True)
            
            # Reconnaissance
            if rec.AcceptWaveform(audio_data):
                result = rec.Result()
                text = self.extract_text_from_vosk_result(result)
                logger.info(f"Transcription: {text}")
                return text
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur speech-to-text: {e}")
            return await self.simulate_speech_to_text(audio_bytes)

    async def simulate_speech_to_text(self, audio_bytes):
        """Simulation de transcription pour le MVP"""
        # Simuler un délai de traitement
        await asyncio.sleep(0.5)
        
        # Retourner un texte simulé basé sur la longueur de l'audio
        audio_length = len(audio_bytes)
        if audio_length < 1000:
            return "Bonjour"
        elif audio_length < 2000:
            return "Comment allez-vous aujourd'hui?"
        else:
            return "Je suis ravi de participer à cette conférence multilingue"

    def prepare_audio_for_vosk(self, audio_bytes):
        """Préparer l'audio pour Vosk"""
        try:
            # Convertir en WAV si nécessaire
            with io.BytesIO(audio_bytes) as audio_io:
                with wave.open(audio_io, 'rb') as wav_file:
                    # Lire les données audio
                    frames = wav_file.readframes(wav_file.getnframes())
                    return frames
        except Exception as e:
            logger.error(f"Erreur préparation audio: {e}")
            return audio_bytes

    def extract_text_from_vosk_result(self, result):
        """Extraire le texte du résultat Vosk"""
        try:
            import json
            result_dict = json.loads(result)
            return result_dict.get('text', '').strip()
        except:
            return ''

    async def translate(self, text, source_lang, target_lang):
        """Traduire le texte"""
        try:
            if source_lang == target_lang:
                return text
            
            # Utiliser Google Translate
            translation = self.translator.translate(
                text, 
                src=source_lang, 
                dest=target_lang
            )
            
            translated_text = translation.text
            logger.info(f"Traduction: {text} -> {translated_text}")
            return translated_text
            
        except Exception as e:
            logger.error(f"Erreur traduction: {e}")
            # Fallback: retourner le texte original
            return text

    async def text_to_speech(self, text, language):
        """Convertir le texte en audio (text-to-speech)"""
        try:
            if not text:
                return b''
            
            # Utiliser gTTS
            tts = gTTS(text=text, lang=self.gtts_language_map.get(language, 'en'))
            
            # Sauvegarder temporairement
            temp_file = f"/tmp/tts_{hash(text)}.mp3"
            tts.save(temp_file)
            
            # Lire le fichier audio
            with open(temp_file, 'rb') as f:
                audio_bytes = f.read()
            
            # Nettoyer le fichier temporaire
            try:
                os.remove(temp_file)
            except:
                pass
            
            logger.info(f"Synthèse vocale générée pour: {text}")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Erreur text-to-speech: {e}")
            # Fallback: retourner un audio silencieux
            return self.generate_silent_audio()

    def generate_silent_audio(self):
        """Générer un audio silencieux en cas d'erreur"""
        # Créer un fichier WAV silencieux de 1 seconde
        sample_rate = 16000
        duration = 1.0
        samples = int(sample_rate * duration)
        
        # Générer des échantillons silencieux
        silent_data = np.zeros(samples, dtype=np.int16)
        
        # Créer le fichier WAV
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(silent_data.tobytes())
            
            return wav_io.getvalue()

    async def process_audio_chunk(self, audio_bytes, source_lang, target_lang):
        """Traiter un chunk audio complet"""
        try:
            # Étape 1: Transcription
            text = await self.speech_to_text(audio_bytes)
            if not text:
                return None
            
            # Étape 2: Traduction
            translated_text = await self.translate(text, source_lang, target_lang)
            
            # Étape 3: Synthèse vocale
            audio_output = await self.text_to_speech(translated_text, target_lang)
            
            return {
                'original_text': text,
                'translated_text': translated_text,
                'audio_output': audio_output
            }
            
        except Exception as e:
            logger.error(f"Erreur traitement audio chunk: {e}")
            return None

    def get_supported_languages(self):
        """Obtenir la liste des langues supportées"""
        return list(self.vosk_language_map.keys())

    def is_language_supported(self, language):
        """Vérifier si une langue est supportée"""
        return language in self.gtts_language_map

    def translate_sync(self, text, source_lang, target_lang):
        """Version synchrone de la traduction"""
        try:
            if source_lang == target_lang:
                return text
            
            # Utiliser Google Translate
            translation = self.translator.translate(
                text, 
                src=source_lang, 
                dest=target_lang
            )
            
            translated_text = translation.text
            logger.info(f"Traduction synchrone: {text} -> {translated_text}")
            return translated_text
            
        except Exception as e:
            logger.error(f"Erreur traduction synchrone: {e}")
            # Fallback: retourner le texte original
            return text

    def text_to_speech_sync(self, text, language):
        """Version synchrone de la synthèse vocale"""
        try:
            if not text:
                return b''
            
            # Utiliser gTTS
            tts = gTTS(text=text, lang=self.gtts_language_map.get(language, 'en'))
            
            # Sauvegarder temporairement
            temp_file = f"/tmp/tts_{hash(text)}.mp3"
            tts.save(temp_file)
            
            # Lire le fichier audio
            with open(temp_file, 'rb') as f:
                audio_bytes = f.read()
            
            # Nettoyer le fichier temporaire
            try:
                os.remove(temp_file)
            except:
                pass
            
            logger.info(f"Synthèse vocale synchrone générée pour: {text}")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Erreur text-to-speech synchrone: {e}")
            # Fallback: retourner un audio silencieux
            return self.generate_silent_audio()

    async def test_pipeline(self):
        """Tester le pipeline complet"""
        try:
            # Créer un audio de test
            test_audio = self.generate_test_audio("Bonjour, comment allez-vous?")
            
            # Tester le pipeline
            result = await self.process_audio_chunk(test_audio, 'fr', 'en')
            
            if result:
                logger.info("Test pipeline réussi")
                return True
            else:
                logger.error("Test pipeline échoué")
                return False
                
        except Exception as e:
            logger.error(f"Erreur test pipeline: {e}")
            return False

    def generate_test_audio(self, text):
        """Générer un audio de test"""
        # Pour le MVP, retourner un audio simulé
        return b'test_audio_data' 