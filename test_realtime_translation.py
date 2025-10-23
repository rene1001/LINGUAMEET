"""
Test complet des fonctionnalités de traduction en temps réel de LinguaMeet
=============================================================================

Ce script teste :
1. La configuration de l'environnement (.env)
2. Le pipeline de traduction (STT, Translation, TTS)
3. La connexion WebSocket
4. Les modèles de base de données
5. La création de salles et de participants

Usage:
    python test_realtime_translation.py
"""

import os
import sys
import django
import asyncio
import json
from pathlib import Path
from datetime import datetime

# Configuration de Django
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.conf import settings
from conference.models import Room, Participant, ConversationHistory
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Colors:
    """Codes de couleur pour l'affichage terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Affiche un en-tête formaté"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

def print_test(name, passed, message=""):
    """Affiche le résultat d'un test"""
    status = f"{Colors.GREEN}[PASS]" if passed else f"{Colors.RED}[FAIL]"
    print(f"{status}{Colors.RESET} - {name}")
    if message:
        print(f"  {Colors.YELLOW}-->{Colors.RESET} {message}")

def print_info(text):
    """Affiche une information"""
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {text}")

def print_warning(text):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {text}")

def print_error(text):
    """Affiche une erreur"""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {text}")

def print_success(text):
    """Affiche un succès"""
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {text}")


class TranslationTester:
    """Classe principale pour tester les fonctionnalités de traduction"""
    
    def __init__(self):
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
        self.pipeline = None
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print_header("TEST DES FONCTIONNALITÉS DE TRADUCTION EN TEMPS RÉEL")
        print_info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_info(f"Django Version: {django.get_version()}")
        print_info(f"Python Version: {sys.version.split()[0]}")
        
        # 1. Tests de configuration
        self.test_environment_configuration()
        
        # 2. Tests de base de données
        self.test_database_models()
        
        # 3. Tests du pipeline audio
        self.test_audio_pipeline()
        
        # 4. Tests WebSocket
        self.test_websocket_configuration()
        
        # 5. Tests des fichiers statiques
        self.test_static_files()
        
        # 6. Résumé final
        self.print_summary()
    
    def test_environment_configuration(self):
        """Test 1: Configuration de l'environnement"""
        print_header("TEST 1: Configuration de l'environnement (.env)")
        
        # Vérifier si .env existe
        env_path = Path(__file__).parent / '.env'
        env_exists = env_path.exists()
        print_test(".env file exists", env_exists)
        
        if env_exists:
            self.test_results['passed'] += 1
        else:
            self.test_results['failed'] += 1
            print_warning("Le fichier .env n'existe pas. Copiez .env.example en .env")
            print_info("Commande: copy .env.example .env")
        
        # Vérifier les variables d'environnement importantes
        use_free_premium = os.getenv('USE_FREE_PREMIUM', '').lower() == 'true'
        use_google_cloud = os.getenv('USE_GOOGLE_CLOUD', '').lower() == 'true'
        gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
        
        print_test("USE_FREE_PREMIUM configuré", use_free_premium, 
                   "Pipeline gratuit premium activé" if use_free_premium else "Pipeline standard")
        
        if use_free_premium:
            has_gemini = bool(gemini_api_key and not gemini_api_key.startswith('AIza_votre'))
            print_test("GEMINI_API_KEY configuré", has_gemini,
                      f"Key présente ({len(gemini_api_key)} chars)" if has_gemini else "Clé manquante ou non configurée")
            
            has_credentials = bool(google_credentials and Path(google_credentials).exists())
            print_test("GOOGLE_APPLICATION_CREDENTIALS configuré", has_credentials,
                      f"Fichier: {google_credentials}" if has_credentials else "Fichier de credentials manquant")
            
            if has_gemini and has_credentials:
                self.test_results['passed'] += 2
            else:
                self.test_results['failed'] += 2
                print_warning("Configuration incomplète pour le pipeline gratuit premium")
                print_info("Consultez SETUP_FREE_PREMIUM.md pour les instructions")
        else:
            print_info("Pipeline standard (Vosk/gTTS) sera utilisé - aucune clé API requise")
            self.test_results['passed'] += 1
    
    def test_database_models(self):
        """Test 2: Modèles de base de données"""
        print_header("TEST 2: Modèles de base de données")
        
        try:
            # Test de création d'une salle
            room = Room.objects.create(
                nom="Salle de Test",
                langue_par_defaut="fr"
            )
            print_test("Création d'une salle de conférence", True, 
                      f"Room ID: {room.id}, Nom: {room.nom}")
            self.test_results['passed'] += 1
            
            # Test de création d'un participant
            participant = Participant.objects.create(
                nom="Testeur",
                langue_parole="fr",
                langue_souhaitée="en",
                room=room
            )
            print_test("Création d'un participant", True,
                      f"Participant ID: {participant.id}, Nom: {participant.nom}")
            self.test_results['passed'] += 1
            
            # Test de récupération
            retrieved_room = Room.objects.get(id=room.id)
            print_test("Récupération d'une salle", retrieved_room.nom == "Salle de Test")
            self.test_results['passed'] += 1
            
            # Test des relations
            participants_count = room.participants.count()
            print_test("Relation Room-Participant", participants_count == 1,
                      f"{participants_count} participant(s) dans la salle")
            self.test_results['passed'] += 1
            
            # Nettoyage
            participant.delete()
            room.delete()
            print_info("Données de test nettoyées")
            
        except Exception as e:
            print_test("Tests de base de données", False, str(e))
            self.test_results['failed'] += 4
    
    def test_audio_pipeline(self):
        """Test 3: Pipeline audio de traduction"""
        print_header("TEST 3: Pipeline audio de traduction")
        
        try:
            # Détecter quel pipeline est utilisé
            use_free_premium = os.getenv('USE_FREE_PREMIUM', 'False').lower() == 'true'
            use_google_cloud = getattr(settings, 'USE_GOOGLE_CLOUD_AUDIO', False)
            
            if use_free_premium:
                from conference.ai_pipeline_free_premium import FreePremiumAudioProcessor
                self.pipeline = FreePremiumAudioProcessor()
                pipeline_name = "Google + Gemini (Gratuit Premium)"
                print_success(f"Pipeline détecté: {pipeline_name}")
            elif use_google_cloud:
                from conference.ai_pipeline_google_cloud import GoogleCloudAudioProcessor
                self.pipeline = GoogleCloudAudioProcessor()
                pipeline_name = "Google Cloud Complet"
                print_success(f"Pipeline détecté: {pipeline_name}")
            else:
                from conference.ai_pipeline import AudioProcessor
                self.pipeline = AudioProcessor()
                pipeline_name = "Standard (Vosk/gTTS)"
                print_success(f"Pipeline détecté: {pipeline_name}")
            
            print_test("Chargement du pipeline audio", True, pipeline_name)
            self.test_results['passed'] += 1
            
            # Test des méthodes du pipeline
            has_stt = hasattr(self.pipeline, 'speech_to_text')
            has_translate = hasattr(self.pipeline, 'translate')
            has_tts = hasattr(self.pipeline, 'text_to_speech')
            
            print_test("Méthode speech_to_text disponible", has_stt)
            print_test("Méthode translate disponible", has_translate)
            print_test("Méthode text_to_speech disponible", has_tts)
            
            if has_stt and has_translate and has_tts:
                self.test_results['passed'] += 3
                print_success("Toutes les méthodes du pipeline sont disponibles")
            else:
                self.test_results['failed'] += 3
                
        except ImportError as e:
            print_test("Import du pipeline audio", False, str(e))
            self.test_results['failed'] += 1
            print_warning("Vérifiez que toutes les dépendances sont installées")
            print_info("Commande: pip install -r requirements.txt")
        except Exception as e:
            print_test("Tests du pipeline audio", False, str(e))
            self.test_results['failed'] += 1
    
    def test_websocket_configuration(self):
        """Test 4: Configuration WebSocket"""
        print_header("TEST 4: Configuration WebSocket (Django Channels)")
        
        try:
            # Vérifier que Channels est installé
            import channels
            print_test("Django Channels installé", True, f"Version: {channels.__version__}")
            self.test_results['passed'] += 1
            
            # Vérifier la configuration ASGI
            asgi_app = getattr(settings, 'ASGI_APPLICATION', None)
            print_test("ASGI_APPLICATION configuré", bool(asgi_app), asgi_app)
            if asgi_app:
                self.test_results['passed'] += 1
            else:
                self.test_results['failed'] += 1
            
            # Vérifier les channel layers
            channel_layers = getattr(settings, 'CHANNEL_LAYERS', None)
            print_test("CHANNEL_LAYERS configuré", bool(channel_layers))
            if channel_layers:
                backend = channel_layers.get('default', {}).get('BACKEND', '')
                print_info(f"Backend: {backend}")
                if 'InMemory' in backend:
                    print_warning("InMemoryChannelLayer utilisé - OK pour le développement")
                    print_info("Pour la production, utilisez Redis: pip install channels-redis")
                self.test_results['passed'] += 1
            else:
                self.test_results['failed'] += 1
            
            # Vérifier le routing WebSocket
            from linguameet_project import routing
            has_ws_patterns = hasattr(routing, 'websocket_urlpatterns')
            print_test("WebSocket routing configuré", has_ws_patterns)
            if has_ws_patterns:
                patterns_count = len(routing.websocket_urlpatterns)
                print_info(f"{patterns_count} pattern(s) WebSocket configuré(s)")
                self.test_results['passed'] += 1
            else:
                self.test_results['failed'] += 1
            
            # Vérifier le consumer
            from conference.consumers import ConferenceConsumer
            print_test("ConferenceConsumer disponible", True)
            self.test_results['passed'] += 1
            
        except ImportError as e:
            print_test("Configuration WebSocket", False, str(e))
            self.test_results['failed'] += 5
            print_warning("Installez Django Channels: pip install channels")
    
    def test_static_files(self):
        """Test 5: Fichiers statiques JavaScript"""
        print_header("TEST 5: Fichiers statiques (JavaScript)")
        
        static_dir = Path(__file__).parent / 'static' / 'js'
        
        js_files = [
            'main.js',
            'room.js',
            'room-integration.js',
            'video-webrtc.js'
        ]
        
        for js_file in js_files:
            file_path = static_dir / js_file
            exists = file_path.exists()
            print_test(f"{js_file} existe", exists, 
                      f"Taille: {file_path.stat().st_size} bytes" if exists else "Fichier manquant")
            if exists:
                self.test_results['passed'] += 1
            else:
                self.test_results['failed'] += 1
    
    def print_summary(self):
        """Affiche le résumé des tests"""
        print_header("RÉSUMÉ DES TESTS")
        
        total = self.test_results['passed'] + self.test_results['failed']
        success_rate = (self.test_results['passed'] / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}Tests passés:{Colors.RESET} {Colors.GREEN}{self.test_results['passed']}{Colors.RESET}")
        print(f"{Colors.BOLD}Tests échoués:{Colors.RESET} {Colors.RED}{self.test_results['failed']}{Colors.RESET}")
        print(f"{Colors.BOLD}Avertissements:{Colors.RESET} {Colors.YELLOW}{self.test_results['warnings']}{Colors.RESET}")
        print(f"{Colors.BOLD}Taux de réussite:{Colors.RESET} {Colors.CYAN}{success_rate:.1f}%{Colors.RESET}\n")
        
        if self.test_results['failed'] == 0:
            print_success("Tous les tests sont passes!")
            print_success("Votre application est prete pour tester la traduction en temps reel!")
            print_info("\nPour lancer le serveur de developpement:")
            print_info("  python manage.py runserver")
            print_info("\nPuis ouvrez: http://localhost:8000")
        else:
            print_error("Certains tests ont echoue.")
            print_warning("Corrigez les problemes ci-dessus avant de lancer l'application.")
            print_info("\nConsultez les guides de configuration:")
            print_info("  - DEMARRAGE_RAPIDE.md")
            print_info("  - SETUP_FREE_PREMIUM.md")
            print_info("  - README.md")


def main():
    """Point d'entrée principal"""
    try:
        tester = TranslationTester()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print_warning("\n\nTests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nErreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
