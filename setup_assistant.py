"""
Assistant de Configuration Google Cloud
Guide interactif pour atteindre 100%
"""

import os
import sys
from dotenv import load_dotenv

# Encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def print_step(number, title):
    print(f"\n{'='*70}")
    print(f"ETAPE {number} : {title}")
    print(f"{'='*70}\n")

def wait_for_user():
    input("\nAppuyez sur Entree quand c'est fait...")

def check_env_var(var_name):
    value = os.getenv(var_name)
    return value is not None and value != ""

def check_file_exists(path):
    return os.path.exists(path)

# État de la configuration
print_header("ASSISTANT DE CONFIGURATION LINGUAMEET")
print("Cet assistant va vous guider pour atteindre 100% de configuration")
print("\nEtat actuel :")
print("-" * 70)

# Vérifier l'état actuel
gemini_ok = check_env_var('GEMINI_API_KEY')
google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
google_creds_ok = google_creds and check_file_exists(google_creds)

progress = 0
if gemini_ok:
    progress += 50
    print("[OK] Gemini API configure (50%)")
else:
    print("[X] Gemini API manquant (0%)")

if google_creds_ok:
    progress += 50
    print("[OK] Google Cloud configure (50%)")
else:
    print("[...] Google Cloud a configurer (0%)")

print(f"\nProgression totale : {progress}%")
print("=" * int(70 * progress / 100) + ">" + " " * int(70 * (100 - progress) / 100))

if progress == 100:
    print("\n[OK] CONFIGURATION COMPLETE A 100% !")
    print("Lancez : python manage.py runserver")
    sys.exit(0)

print("\nVous etes actuellement a " + str(progress) + "%")
print("Objectif : 100%")

input("\nAppuyez sur Entree pour continuer...")

# Guide étape par étape
print_step(1, "Créer un Projet Google Cloud")
print("1. Ouvrez ce lien dans votre navigateur :")
print("   https://console.cloud.google.com")
print("\n2. Cliquez sur 'Selectionner un projet' (en haut a gauche)")
print("3. Cliquez sur 'Nouveau projet'")
print("4. Nom du projet : linguameet-free")
print("5. Cliquez sur 'Creer'")
print("6. Attendez 10 secondes")
print("7. Selectionnez le projet cree")

wait_for_user()

print_step(2, "Activer Speech-to-Text API")
print("1. Ouvrez ce lien :")
print("   https://console.cloud.google.com/apis/library/speech.googleapis.com")
print("\n2. Verifiez que votre projet 'linguameet-free' est selectionne (en haut)")
print("3. Cliquez sur 'ACTIVER'")
print("4. Attendez quelques secondes")

wait_for_user()

print_step(3, "Activer Text-to-Speech API")
print("1. Ouvrez ce lien :")
print("   https://console.cloud.google.com/apis/library/texttospeech.googleapis.com")
print("\n2. Cliquez sur 'ACTIVER'")
print("3. Attendez quelques secondes")

wait_for_user()

print_step(4, "Créer un Compte de Service")
print("1. Ouvrez ce lien :")
print("   https://console.cloud.google.com/iam-admin/serviceaccounts")
print("\n2. Cliquez sur 'CREER UN COMPTE DE SERVICE' (en haut)")
print("\n3. Etape 1 - Details :")
print("   - Nom : linguameet-service")
print("   - Cliquez sur 'CREER ET CONTINUER'")
print("\n4. Etape 2 - Roles :")
print("   - Cliquez sur 'Selectionner un role'")
print("   - Cherchez : Cloud Speech Client")
print("   - Selectionnez-le")
print("   - Cliquez sur '+ AJOUTER UN AUTRE ROLE'")
print("   - Cherchez : Cloud Text-to-Speech User")
print("   - Selectionnez-le")
print("   - Cliquez sur 'CONTINUER'")
print("\n5. Etape 3 - Acces utilisateurs :")
print("   - Laissez vide")
print("   - Cliquez sur 'TERMINE'")

wait_for_user()

print_step(5, "Télécharger la Clé JSON")
print("1. Dans la liste des comptes de service,")
print("   CLIQUEZ sur 'linguameet-service@...'")
print("\n2. Allez dans l'onglet 'CLES' (en haut)")
print("\n3. Cliquez sur 'AJOUTER UNE CLE' -> 'Creer une cle'")
print("\n4. Type : JSON (deja selectionne)")
print("\n5. Cliquez sur 'CREER'")
print("\n[INFO] Un fichier JSON est telecharge dans votre dossier Telechargements")

wait_for_user()

print_step(6, "Placer la Clé dans le Projet")
print("Nous allons deplacer le fichier JSON telecharge.")
print("\nOption 1 - Automatique :")
print("Tapez cette commande dans une autre fenetre PowerShell :")
print()
print("move C:\\Users\\%USERNAME%\\Downloads\\linguameet-free-*.json c:\\wamp64\\www\\LangMeet\\LINGUAMEET\\credentials\\google-cloud-key.json")
print()
print("\nOption 2 - Manuel :")
print("1. Ouvrez le dossier Telechargements")
print("2. Coupez le fichier linguameet-free-xxxxx.json")
print("3. Collez dans : c:\\wamp64\\www\\LangMeet\\LINGUAMEET\\credentials\\")
print("4. Renommez en : google-cloud-key.json")

wait_for_user()

# Vérifier que le fichier existe
creds_path = r"c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json"
if check_file_exists(creds_path):
    print("[OK] Fichier google-cloud-key.json trouve !")
else:
    print("[X] Fichier google-cloud-key.json NON trouve")
    print("Verifiez l'emplacement et reessayez")
    wait_for_user()

print_step(7, "Activer dans .env")
print("Maintenant, nous devons activer la configuration.")
print("\n1. Ouvrez le fichier : .env")
print("   (dans c:\\wamp64\\www\\LangMeet\\LINGUAMEET\\)")
print("\n2. Cherchez cette ligne :")
print("   # GOOGLE_APPLICATION_CREDENTIALS=...")
print("\n3. ENLEVEZ le # au debut de la ligne")
print("\n4. La ligne doit ressembler a :")
print("   GOOGLE_APPLICATION_CREDENTIALS=c:\\wamp64\\www\\LangMeet\\LINGUAMEET\\credentials\\google-cloud-key.json")
print("\n5. Sauvegardez le fichier (Ctrl+S)")

wait_for_user()

print_step(8, "TEST FINAL")
print("Nous allons maintenant tester la configuration complete...")
print()

input("Appuyez sur Entree pour lancer le test...")

# Recharger les variables d'environnement
load_dotenv(override=True)

print("\nLancement du test...\n")
os.system("python test_config.py")

print("\n" + "=" * 70)
print("CONFIGURATION TERMINEE !")
print("=" * 70)

print("\nSi le test montre [OK] partout, vous etes a 100% !")
print("\nPour lancer LinguaMeet :")
print("  python manage.py runserver")
print("\nPuis ouvrez : http://localhost:8000")
print("\nBonne utilisation ! 🚀")
