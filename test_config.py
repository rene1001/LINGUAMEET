"""
Script de test pour vérifier la configuration LinguaMeet
"""

import os
import sys
from dotenv import load_dotenv

# Charger .env
load_dotenv()

# Encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("TEST DE CONFIGURATION LINGUAMEET")
print("=" * 60)
print()

# Test 1: Vérifier les variables d'environnement
print("1. Variables d'environnement:")
print("-" * 60)

use_free_premium = os.getenv('USE_FREE_PREMIUM', 'False')
gemini_key = os.getenv('GEMINI_API_KEY')
google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

print(f"USE_FREE_PREMIUM: {use_free_premium}")
print(f"GEMINI_API_KEY: {'[OK] Definie' if gemini_key else '[X] Manquante'}")
if gemini_key:
    print(f"  -> {gemini_key[:20]}...")
print(f"GOOGLE_APPLICATION_CREDENTIALS: {'[OK] Definie' if google_creds else '[X] Manquante'}")
if google_creds:
    print(f"  -> {google_creds}")
    if os.path.exists(google_creds):
        print(f"  -> [OK] Fichier existe")
    else:
        print(f"  -> [X] Fichier n'existe pas")
print()

# Test 2: Tester Gemini
print("2. Test Gemini API:")
print("-" * 60)

if gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        # Utiliser gemini-2.5-flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("Envoi d'une requete test a Gemini...")
        response = model.generate_content("Traduis en anglais : Bonjour")
        
        print(f"[OK] Gemini fonctionne !")
        print(f"Reponse : {response.text}")
    except Exception as e:
        print(f"[X] Erreur Gemini : {e}")
else:
    print("[X] Cle Gemini non configuree")
print()

# Test 3: Tester Google Cloud (si configuré)
print("3. Test Google Cloud:")
print("-" * 60)

if google_creds and os.path.exists(google_creds):
    try:
        from google.cloud import speech
        from google.cloud import texttospeech
        
        print("Initialisation Speech-to-Text...")
        speech_client = speech.SpeechClient()
        print("[OK] Google Speech-to-Text OK")
        
        print("Initialisation Text-to-Speech...")
        tts_client = texttospeech.TextToSpeechClient()
        print("[OK] Google Text-to-Speech OK")
        
    except Exception as e:
        print(f"[X] Erreur Google Cloud : {e}")
        print("\nSi vous voyez 'could not find default credentials',")
        print("suivez le guide de configuration pour configurer Google Cloud")
else:
    print("[...] Google Cloud pas encore configure")
    print("\nPour activer :")
    print("1. Suivre le guide de configuration")
    print("2. Obtenir cle JSON de Google Cloud")
    print("3. Placer dans credentials/google-cloud-key.json")
    print("4. Decommenter GOOGLE_APPLICATION_CREDENTIALS dans .env")
print()

# Test 4: État du pipeline
print("4. Pipeline Audio:")
print("-" * 60)

if use_free_premium.lower() == 'true':
    if gemini_key and google_creds and os.path.exists(google_creds):
        print("[OK] Pipeline Google + Gemini : ACTIF")
        print("   -> Google Speech-to-Text (transcription)")
        print("   -> Gemini AI (traduction)")
        print("   -> Google TTS (synthese vocale)")
    elif gemini_key:
        print("[!] Pipeline PARTIEL : Gemini seul")
        print("   -> Gemini configure [OK]")
        print("   -> Google Cloud manquant [X]")
        print("\n[INFO] Suivez le guide de configuration pour activer Google Cloud")
    else:
        print("[X] Pipeline non configure")
else:
    print("[*] Pipeline Standard (Vosk/gTTS)")
print()

# Résumé
print("=" * 60)
print("RESUME")
print("=" * 60)

status = []
if use_free_premium.lower() == 'true':
    status.append("[OK] Mode Google + Gemini actif")
else:
    status.append("[*] Mode Standard (Vosk/gTTS)")

if gemini_key:
    status.append("[OK] Gemini API configure")
else:
    status.append("[X] Gemini API manquant")

if google_creds and os.path.exists(google_creds):
    status.append("[OK] Google Cloud configure")
else:
    status.append("[...] Google Cloud a configurer")

for s in status:
    print(s)

print()
print("=" * 60)

# Prochaines étapes
if not gemini_key:
    print("\nPROCHAINE ETAPE :")
    print("Obtenez une cle Gemini sur : https://makersuite.google.com/app/apikey")
elif not (google_creds and os.path.exists(google_creds)):
    print("\nPROCHAINE ETAPE :")
    print("Configurez Google Cloud (15 min)")
else:
    print("\nTOUT EST CONFIGURE !")
    print("Lancez le serveur : python manage.py runserver")

print()
