"""
Pipeline Audio de QUALITÉ PROFESSIONNELLE
Utilise les APIs de :
- Google Speech-to-Text (60 min/mois)
- Gemini API (60 req/min)
- Google TTS (1M chars/mois)

Parfait pour étudiants ! 🎓
"""

import asyncio
import io
import os
import logging
import google.generativeai as genai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech

logger = logging.getLogger(__name__)


class FreePremiumAudioProcessor:
    """
    Pipeline audio professionnel
    Utilise les APIs de Google et Gemini
    """
    
    def __init__(self):
        self.is_ready = False
        
        try:
            # 1. Google Speech-to-Text (60 min/mois)
            self.speech_client = speech.SpeechClient()
            logger.info("✅ Google Speech-to-Text initialisé")
            
            # 2. Gemini API pour traduction (60 req/min)
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key:
                genai.configure(api_key=gemini_key)
                # Utiliser gemini-2.5-flash
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("✅ Gemini API initialisé (gemini-2.5-flash)")
            else:
                logger.warning("⚠️ GEMINI_API_KEY non défini")
                self.gemini_model = None
            
            # 3. Google TTS (1M chars/mois)
            self.tts_client = texttospeech.TextToSpeechClient()
            logger.info("✅ Google Text-to-Speech initialisé")
            
            self.is_ready = True
            logger.info("🎉 Pipeline audio prêt !")
            
        except Exception as e:
            logger.error(f"❌ Erreur initialisation: {e}")
            logger.error("Vérifiez GOOGLE_APPLICATION_CREDENTIALS et GEMINI_API_KEY")
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
        
        # Noms de langues pour Gemini
        self.language_names = {
            'fr': 'français',
            'en': 'anglais',
            'es': 'espagnol',
            'de': 'allemand',
            'it': 'italien',
            'pt': 'portugais',
            'ru': 'russe',
            'ja': 'japonais',
            'ko': 'coréen',
            'zh': 'chinois'
        }
        
        # Voix Standard Google TTS (1M chars/mois)
        self.optimal_voices = {
            'fr': 'fr-FR-Standard-A',
            'en': 'en-US-Standard-J',
            'es': 'es-ES-Standard-A',
            'de': 'de-DE-Standard-F',
            'it': 'it-IT-Standard-A',
            'pt': 'pt-PT-Standard-A',
            'ru': 'ru-RU-Standard-A',
            'ja': 'ja-JP-Standard-B',
            'ko': 'ko-KR-Standard-A',
            'zh': 'cmn-CN-Standard-A'
        }

    async def speech_to_text(self, audio_bytes, source_language='fr'):
        """
        Speech-to-Text avec Google Cloud
        Quota : 60 minutes/mois
        
        Args:
            audio_bytes: Audio en bytes
            source_language: Langue source
        
        Returns:
            str: Texte transcrit
        """
        if not self.is_ready:
            logger.error("Pipeline non initialisé")
            return None
        
        try:
            # Préparer l'audio
            audio = speech.RecognitionAudio(content=audio_bytes)
            
            # Configuration
            language_code = self.language_codes.get(source_language, 'fr-FR')
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
                model="default",  # Modèle par défaut
                use_enhanced=False  # Version standard
            )
            
            # Reconnaissance
            response = await asyncio.to_thread(
                self.speech_client.recognize,
                config=config,
                audio=audio
            )
            
            # Extraire le texte
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            transcript = transcript.strip()
            
            if transcript:
                logger.info(f"🎤 Transcription: {transcript}")
                return transcript
            else:
                logger.warning("Aucune transcription")
                return None
            
        except Exception as e:
            logger.error(f"Erreur STT: {e}")
            return None

    async def translate(self, text, source_lang, target_lang):
        """
        Traduction avec Gemini API
        Quota : 60 requêtes/minute
        
        Args:
            text: Texte à traduire
            source_lang: Langue source
            target_lang: Langue cible
        
        Returns:
            str: Texte traduit
        """
        return await self.translate_with_gemini(text, source_lang, target_lang)
    
    async def translate_with_gemini(self, text, source_lang, target_lang):
        """
        Traduction avec Gemini API (méthode interne)
        Quota : 60 requêtes/minute
        
        Args:
            text: Texte à traduire
            source_lang: Langue source
            target_lang: Langue cible
        
        Returns:
            str: Texte traduit
        """
        if not self.gemini_model:
            logger.error("Gemini non configuré")
            return text
        
        try:
            if source_lang == target_lang:
                return text
            
            source_name = self.language_names.get(source_lang, source_lang)
            target_name = self.language_names.get(target_lang, target_lang)
            
            # Prompt optimisé pour traduction fluide
            prompt = f"""Tu es un traducteur professionnel expert.

Traduis cette phrase de {source_name} vers {target_name}.

RÈGLES IMPORTANTES :
- Traduis de manière NATURELLE et FLUIDE
- Préserve le TON et l'INTENTION du message
- Adapte les expressions idiomatiques
- Ne réponds QUE par la traduction, rien d'autre
- Pas d'explications, pas de commentaires

Texte à traduire : "{text}"

Traduction :"""
            
            # Appel à Gemini
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Cohérence
                    max_output_tokens=500
                )
            )
            
            translated = response.text.strip()
            
            # Nettoyer la réponse (enlever guillemets si présents)
            translated = translated.strip('"\'')
            
            logger.info(f"🌍 Traduction Gemini: {text[:50]}... → {translated[:50]}...")
            
            return translated
            
        except Exception as e:
            logger.error(f"Erreur Gemini: {e}")
            # Fallback : retourner texte original
            return text

    async def text_to_speech(self, text, target_language='en'):
        """
        Text-to-Speech avec Google Cloud
        Quota : 1 million de caractères/mois (Standard)
        
        Args:
            text: Texte à synthétiser
            target_language: Langue cible
        
        Returns:
            bytes: Audio MP3
        """
        if not self.is_ready:
            logger.error("Pipeline non initialisé")
            return b''
        
        try:
            if not text:
                return b''
            
            # Préparer le texte
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Voix STANDARD
            voice_name = self.optimal_voices.get(target_language, 'en-US-Standard-J')
            language_code = self.language_codes.get(target_language, 'en-US')
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )
            
            # Configuration audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0.0,
                volume_gain_db=0.0,
                sample_rate_hertz=24000
            )
            
            # Synthèse
            response = await asyncio.to_thread(
                self.tts_client.synthesize_speech,
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            audio_bytes = response.audio_content
            
            logger.info(f"🔊 TTS généré: {len(audio_bytes)} bytes")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Erreur TTS: {e}")
            return b''

    async def process_audio_chunk(self, audio_bytes, source_lang, target_lang):
        """
        Pipeline complet : Audio → Audio traduit
        
        Utilise :
        - Google STT (60 min/mois)
        - Gemini (60 req/min)
        - Google TTS (1M chars/mois)
        
        Args:
            audio_bytes: Audio d'entrée
            source_lang: Langue source
            target_lang: Langue cible
        
        Returns:
            dict: Résultat complet
        """
        try:
            logger.info(f"📥 Pipeline démarré: {source_lang} → {target_lang}")
            
            # Étape 1: Speech-to-Text (Google - 60 min/mois)
            original_text = await self.speech_to_text(audio_bytes, source_lang)
            if not original_text:
                logger.warning("Aucun texte transcrit")
                return None
            
            # Étape 2: Traduction (Gemini - 60 req/min)
            translated_text = await self.translate_with_gemini(
                original_text,
                source_lang,
                target_lang
            )
            
            # Étape 3: Text-to-Speech (Google - 1M chars/mois)
            audio_output = await self.text_to_speech(translated_text, target_lang)
            
            logger.info(f"✅ Pipeline terminé !")
            
            return {
                'original_text': original_text,
                'translated_text': translated_text,
                'audio_output': audio_output,
                'source_language': source_lang,
                'target_language': target_lang
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur pipeline: {e}")
            return None

    async def test_pipeline(self):
        """Test du pipeline"""
        try:
            logger.info("🧪 Test du pipeline...")
            
            # Créer un audio de test
            from gtts import gTTS
            import tempfile
            
            test_text = "Bonjour, ceci est un test de traduction"
            tts = gTTS(text=test_text, lang='fr')
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_path = f.name
                tts.save(temp_path)
            
            with open(temp_path, 'rb') as f:
                test_audio = f.read()
            
            os.remove(temp_path)
            
            # Tester
            result = await self.process_audio_chunk(test_audio, 'fr', 'en')
            
            if result:
                logger.info(f"✅ Test réussi!")
                logger.info(f"   Original: {result['original_text']}")
                logger.info(f"   Traduit: {result['translated_text']}")
                logger.info(f"   Audio: {len(result['audio_output'])} bytes")
                return True
            else:
                logger.error("❌ Test échoué")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur test: {e}")
            return False


# Fonction pour obtenir le bon processeur
def get_audio_processor_smart():
    """
    Retourne le meilleur processeur selon la config
    
    Priorité :
    1. Pipeline Google + Gemini (si credentials disponibles)
    2. Vosk/gTTS (fallback basique)
    """
    # Vérifier si on a les credentials pour le pipeline Google + Gemini
    has_google_creds = bool(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    has_gemini_key = bool(os.getenv('GEMINI_API_KEY'))
    
    if has_google_creds and has_gemini_key:
        logger.info("🎓 Utilisation du pipeline Google + Gemini")
        return FreePremiumAudioProcessor()
    else:
        logger.info("📦 Fallback vers pipeline standard (Vosk/gTTS)")
        from .ai_pipeline import AudioProcessor
        return AudioProcessor()


if __name__ == "__main__":
    async def main():
        processor = FreePremiumAudioProcessor()
        await processor.test_pipeline()
    
    asyncio.run(main())
