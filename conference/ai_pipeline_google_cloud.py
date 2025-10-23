"""
Pipeline Audio avec Google Cloud APIs - Version Professionnelle
Utilise : Cloud Speech-to-Text, Cloud Translation, Cloud Text-to-Speech

Pour activer ce pipeline :
1. Installer : pip install google-cloud-speech google-cloud-translate google-cloud-texttospeech
2. Créer un projet Google Cloud
3. Activer les 3 APIs
4. Télécharger la clé de service JSON
5. Définir : GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
"""

import asyncio
import io
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import logging

logger = logging.getLogger(__name__)


class GoogleCloudAudioProcessor:
    """Pipeline audio professionnel avec Google Cloud APIs"""
    
    def __init__(self):
        try:
            # Initialiser les clients Google Cloud
            self.speech_client = speech.SpeechClient()
            self.translate_client = translate.Client()
            self.tts_client = texttospeech.TextToSpeechClient()
            
            logger.info("✅ Google Cloud APIs initialisées avec succès")
            self.is_ready = True
            
        except Exception as e:
            logger.error(f"❌ Erreur initialisation Google Cloud: {e}")
            logger.error("Vérifiez GOOGLE_APPLICATION_CREDENTIALS")
            self.is_ready = False
        
        # Configuration des langues
        self.language_codes = {
            'fr': 'fr-FR',
            'en': 'en-US',
            'es': 'es-ES',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-PT',
            'ru': 'ru-RU',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'zh': 'zh-CN'
        }
        
        # Voix optimales pour chaque langue (Neural2 - meilleure qualité)
        self.optimal_voices = {
            'fr': 'fr-FR-Neural2-A',
            'en': 'en-US-Neural2-J',
            'es': 'es-ES-Neural2-A',
            'de': 'de-DE-Neural2-F',
            'it': 'it-IT-Neural2-A',
            'pt': 'pt-PT-Neural2-A',
            'ru': 'ru-RU-Wavenet-A',  # Neural2 pas encore dispo
            'ja': 'ja-JP-Neural2-B',
            'ko': 'ko-KR-Neural2-A',
            'zh': 'zh-CN-Neural2-A'
        }

    async def speech_to_text(self, audio_bytes, source_language='fr'):
        """
        Convertir l'audio en texte avec Google Cloud Speech-to-Text
        
        Args:
            audio_bytes: Données audio en bytes (WAV/MP3)
            source_language: Code langue source ('fr', 'en', etc.)
        
        Returns:
            str: Texte transcrit
        """
        if not self.is_ready:
            logger.error("Google Cloud non initialisé")
            return None
        
        try:
            # Préparer l'audio
            audio = speech.RecognitionAudio(content=audio_bytes)
            
            # Configuration de la reconnaissance
            language_code = self.language_codes.get(source_language, 'fr-FR')
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
                model="latest_long",  # Meilleur modèle
                use_enhanced=True,  # Modèle amélioré
                # Alternative languages pour meilleure détection
                alternative_language_codes=[
                    self.language_codes.get(l) 
                    for l in ['en', 'es', 'de'] 
                    if l != source_language
                ][:2]
            )
            
            # Reconnaissance asynchrone
            operation = self.speech_client.long_running_recognize(
                config=config,
                audio=audio
            )
            
            # Attendre le résultat (avec timeout)
            response = await asyncio.wait_for(
                asyncio.to_thread(operation.result),
                timeout=10.0
            )
            
            # Extraire le texte
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            transcript = transcript.strip()
            
            if transcript:
                logger.info(f"🎤 Transcription ({source_language}): {transcript}")
                return transcript
            else:
                logger.warning("Aucune transcription détectée")
                return None
            
        except asyncio.TimeoutError:
            logger.error("Timeout lors de la transcription")
            return None
        except Exception as e:
            logger.error(f"Erreur speech-to-text: {e}")
            return None

    async def speech_to_text_streaming(self, audio_stream, source_language='fr'):
        """
        Version streaming pour transcription en temps réel
        Utilisable pour conversations longues
        """
        if not self.is_ready:
            return None
        
        try:
            language_code = self.language_codes.get(source_language, 'fr-FR')
            
            streaming_config = speech.StreamingRecognitionConfig(
                config=speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code=language_code,
                    enable_automatic_punctuation=True,
                ),
                interim_results=True  # Résultats intermédiaires
            )
            
            # Cette méthode retourne un générateur pour le streaming
            # À implémenter selon vos besoins
            pass
            
        except Exception as e:
            logger.error(f"Erreur streaming STT: {e}")
            return None

    async def translate(self, text, source_lang, target_lang):
        """
        Traduire le texte avec Google Cloud Translation API
        
        Args:
            text: Texte à traduire
            source_lang: Langue source ('fr', 'en', etc.)
            target_lang: Langue cible
        
        Returns:
            str: Texte traduit
        """
        if not self.is_ready:
            logger.error("Google Cloud non initialisé")
            return text
        
        try:
            # Si même langue, pas besoin de traduction
            if source_lang == target_lang:
                return text
            
            # Traduction
            result = await asyncio.to_thread(
                self.translate_client.translate,
                text,
                source_language=source_lang,
                target_language=target_lang,
                format_='text'
            )
            
            translated_text = result['translatedText']
            
            logger.info(f"🌍 Traduction ({source_lang}→{target_lang}): {text[:50]}... → {translated_text[:50]}...")
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Erreur traduction: {e}")
            # Fallback: retourner le texte original
            return text

    async def text_to_speech(self, text, target_language='en'):
        """
        Convertir le texte en audio avec Google Cloud Text-to-Speech
        
        Args:
            text: Texte à synthétiser
            target_language: Langue cible ('fr', 'en', etc.)
        
        Returns:
            bytes: Audio MP3
        """
        if not self.is_ready:
            logger.error("Google Cloud non initialisé")
            return b''
        
        try:
            if not text:
                return b''
            
            # Préparer le texte
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Sélectionner la meilleure voix pour la langue
            voice_name = self.optimal_voices.get(target_language, 'en-US-Neural2-J')
            language_code = self.language_codes.get(target_language, 'en-US')
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )
            
            # Configuration audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,  # Vitesse normale (0.25 à 4.0)
                pitch=0.0,  # Ton normal (-20.0 à 20.0)
                volume_gain_db=0.0,  # Volume normal
                sample_rate_hertz=24000  # Haute qualité
            )
            
            # Synthèse
            response = await asyncio.to_thread(
                self.tts_client.synthesize_speech,
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            audio_bytes = response.audio_content
            
            logger.info(f"🔊 TTS généré ({target_language}): {len(audio_bytes)} bytes")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Erreur text-to-speech: {e}")
            return b''

    async def process_audio_chunk(self, audio_bytes, source_lang, target_lang):
        """
        Pipeline complet : Audio source → Audio traduit
        
        Args:
            audio_bytes: Audio d'entrée
            source_lang: Langue source
            target_lang: Langue cible
        
        Returns:
            dict: {
                'original_text': str,
                'translated_text': str,
                'audio_output': bytes
            }
        """
        try:
            # Étape 1: Speech-to-Text
            logger.info(f"📥 Pipeline démarré: {source_lang} → {target_lang}")
            
            original_text = await self.speech_to_text(audio_bytes, source_lang)
            if not original_text:
                logger.warning("Aucun texte transcrit")
                return None
            
            # Étape 2: Traduction
            translated_text = await self.translate(
                original_text,
                source_lang,
                target_lang
            )
            
            # Étape 3: Text-to-Speech
            audio_output = await self.text_to_speech(translated_text, target_lang)
            
            logger.info(f"✅ Pipeline terminé avec succès")
            
            return {
                'original_text': original_text,
                'translated_text': translated_text,
                'audio_output': audio_output,
                'source_language': source_lang,
                'target_language': target_lang
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur pipeline audio: {e}")
            return None

    def get_available_voices(self, language_code='fr-FR'):
        """
        Obtenir toutes les voix disponibles pour une langue
        Utile pour laisser l'utilisateur choisir
        """
        try:
            voices = self.tts_client.list_voices(language_code=language_code)
            
            available = []
            for voice in voices.voices:
                available.append({
                    'name': voice.name,
                    'gender': voice.ssml_gender,
                    'language': voice.language_codes[0]
                })
            
            return available
            
        except Exception as e:
            logger.error(f"Erreur récupération voix: {e}")
            return []

    async def test_pipeline(self):
        """
        Tester le pipeline complet avec un exemple
        """
        try:
            logger.info("🧪 Test du pipeline Google Cloud...")
            
            # Créer un audio de test avec gTTS (temporaire)
            from gtts import gTTS
            import tempfile
            
            test_text = "Bonjour, ceci est un test de traduction audio"
            tts = gTTS(text=test_text, lang='fr')
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_path = f.name
                tts.save(temp_path)
            
            # Lire l'audio de test
            with open(temp_path, 'rb') as f:
                test_audio = f.read()
            
            # Nettoyer
            os.remove(temp_path)
            
            # Tester le pipeline
            result = await self.process_audio_chunk(test_audio, 'fr', 'en')
            
            if result:
                logger.info(f"✅ Test réussi!")
                logger.info(f"   Original: {result['original_text']}")
                logger.info(f"   Traduit: {result['translated_text']}")
                logger.info(f"   Audio généré: {len(result['audio_output'])} bytes")
                return True
            else:
                logger.error("❌ Test échoué")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur test pipeline: {e}")
            return False


# Fonction helper pour basculer entre pipelines
def get_audio_processor(use_google_cloud=False):
    """
    Retourne le processeur audio approprié
    
    Args:
        use_google_cloud: Si True, utilise Google Cloud, sinon Vosk/gTTS
    
    Returns:
        AudioProcessor instance
    """
    if use_google_cloud:
        # Vérifier si les credentials sont configurés
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            logger.warning("⚠️ GOOGLE_APPLICATION_CREDENTIALS non défini, fallback vers Vosk")
            from .ai_pipeline import AudioProcessor
            return AudioProcessor()
        
        return GoogleCloudAudioProcessor()
    else:
        from .ai_pipeline import AudioProcessor
        return AudioProcessor()


# Test direct
if __name__ == "__main__":
    async def main():
        processor = GoogleCloudAudioProcessor()
        await processor.test_pipeline()
    
    asyncio.run(main())
