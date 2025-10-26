"""
Test Approfondi de Google Gemini pour la Traduction
====================================================

Ce script teste en profondeur les capacités de traduction de Gemini
avec plusieurs langues et scénarios différents.

Usage:
    python test_gemini_traduction.py
"""

import os
import sys
import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import google.generativeai as genai

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

def print_success(text):
    """Affiche un succès"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Affiche une erreur"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Affiche une information"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def print_translation(source, target, original, translated, time_ms):
    """Affiche une traduction"""
    print(f"{Colors.BOLD}Traduction {source} → {target}:{Colors.RESET}")
    print(f"  {Colors.YELLOW}Original:{Colors.RESET} {original}")
    print(f"  {Colors.GREEN}Traduit:{Colors.RESET}  {translated}")
    print(f"  {Colors.CYAN}Temps:{Colors.RESET}    {time_ms:.0f}ms\n")


class GeminiTranslationTester:
    """Testeur de traductions Gemini"""
    
    def __init__(self):
        # Configuration Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY non configurée")
        
        genai.configure(api_key=gemini_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Statistiques
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_time = 0
        
        # Noms de langues
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
    
    def translate(self, text, source_lang, target_lang):
        """Traduit un texte avec Gemini"""
        source_name = self.language_names.get(source_lang, source_lang)
        target_name = self.language_names.get(target_lang, target_lang)
        
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
        
        start_time = time.time()
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=500
            )
        )
        end_time = time.time()
        
        translated = response.text.strip().strip('"\'')
        time_ms = (end_time - start_time) * 1000
        
        return translated, time_ms
    
    def test_translation(self, text, source_lang, target_lang, expected_keywords=None):
        """Teste une traduction"""
        self.total_tests += 1
        
        try:
            translated, time_ms = self.translate(text, source_lang, target_lang)
            self.total_time += time_ms
            
            # Vérifier que la traduction n'est pas vide
            if not translated:
                print_error(f"Traduction vide pour: {text}")
                self.failed_tests += 1
                return False
            
            # Vérifier que la traduction est différente de l'original (si langues différentes)
            if source_lang != target_lang and translated.lower() == text.lower():
                print_error(f"Traduction identique à l'original: {text}")
                self.failed_tests += 1
                return False
            
            # Vérifier les mots-clés si fournis
            if expected_keywords:
                found_keywords = sum(1 for kw in expected_keywords if kw.lower() in translated.lower())
                if found_keywords == 0:
                    print_error(f"Aucun mot-clé trouvé dans: {translated}")
                    self.failed_tests += 1
                    return False
            
            print_translation(source_lang, target_lang, text, translated, time_ms)
            self.passed_tests += 1
            return True
            
        except Exception as e:
            print_error(f"Erreur lors de la traduction: {e}")
            self.failed_tests += 1
            return False
    
    def run_basic_tests(self):
        """Tests de base"""
        print_header("TEST 1: Traductions de Base (FR → EN, ES, DE)")
        
        tests = [
            ("Bonjour, comment allez-vous ?", "fr", "en", ["hello", "how"]),
            ("Je suis étudiant en informatique", "fr", "es", ["estudiante", "informática"]),
            ("C'est une belle journée", "fr", "de", ["schön", "tag"]),
        ]
        
        for text, source, target, keywords in tests:
            self.test_translation(text, source, target, keywords)
    
    def run_reverse_tests(self):
        """Tests inverses"""
        print_header("TEST 2: Traductions Inverses (EN, ES → FR)")
        
        tests = [
            ("Hello, how are you today?", "en", "fr", ["bonjour", "comment"]),
            ("The weather is beautiful", "en", "fr", ["temps", "beau"]),
            ("Hola, ¿cómo estás?", "es", "fr", ["bonjour", "salut"]),
        ]
        
        for text, source, target, keywords in tests:
            self.test_translation(text, source, target, keywords)
    
    def run_multilang_tests(self):
        """Tests multilingues"""
        print_header("TEST 3: Traductions Multilingues (diverses langues)")
        
        tests = [
            ("Buongiorno!", "it", "fr", ["bonjour"]),
            ("Guten Morgen", "de", "en", ["morning", "good"]),
            ("Obrigado", "pt", "fr", ["merci"]),
            ("こんにちは", "ja", "en", ["hello"]),
        ]
        
        for text, source, target, keywords in tests:
            self.test_translation(text, source, target, keywords)
    
    def run_long_sentence_tests(self):
        """Tests avec phrases longues"""
        print_header("TEST 4: Phrases Longues et Complexes")
        
        tests = [
            (
                "Je voudrais réserver une table pour deux personnes ce soir à 20 heures dans votre restaurant.",
                "fr", "en",
                ["reserve", "table", "restaurant"]
            ),
            (
                "L'intelligence artificielle révolutionne le monde de la technologie et change notre façon de travailler.",
                "fr", "es",
                ["inteligencia", "artificial"]
            ),
        ]
        
        for text, source, target, keywords in tests:
            self.test_translation(text, source, target, keywords)
    
    def run_colloquial_tests(self):
        """Tests avec expressions familières"""
        print_header("TEST 5: Expressions Familières et Idiomatiques")
        
        tests = [
            ("Ça marche !", "fr", "en", None),
            ("J'ai la flemme", "fr", "en", None),
            ("C'est le pied !", "fr", "en", None),
            ("Break a leg!", "en", "fr", None),
        ]
        
        for text, source, target, keywords in tests:
            self.test_translation(text, source, target, keywords)
    
    def run_speed_test(self):
        """Test de vitesse"""
        print_header("TEST 6: Test de Vitesse (10 traductions rapides)")
        
        text = "Bonjour"
        print_info(f"Traduction de '{text}' FR→EN, 10 fois...")
        
        times = []
        for i in range(10):
            try:
                _, time_ms = self.translate(text, "fr", "en")
                times.append(time_ms)
                print(f"  #{i+1}: {time_ms:.0f}ms", end="\r")
            except Exception as e:
                print_error(f"Erreur #{i+1}: {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n")
            print_success(f"Temps moyen: {avg_time:.0f}ms")
            print_success(f"Temps min: {min_time:.0f}ms")
            print_success(f"Temps max: {max_time:.0f}ms")
    
    def print_summary(self):
        """Affiche le résumé"""
        print_header("RÉSUMÉ DES TESTS GEMINI")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        avg_time = self.total_time / self.total_tests if self.total_tests > 0 else 0
        
        print(f"{Colors.BOLD}Total de tests:{Colors.RESET} {self.total_tests}")
        print(f"{Colors.GREEN}Tests réussis:{Colors.RESET} {self.passed_tests}")
        print(f"{Colors.RED}Tests échoués:{Colors.RESET} {self.failed_tests}")
        print(f"{Colors.CYAN}Taux de réussite:{Colors.RESET} {success_rate:.1f}%")
        print(f"{Colors.CYAN}Temps moyen:{Colors.RESET} {avg_time:.0f}ms par traduction\n")
        
        if self.failed_tests == 0:
            print_success("🎉 Tous les tests Gemini sont passés avec succès !")
            print_success("Le système de traduction fonctionne parfaitement.")
        else:
            print_error(f"⚠️ {self.failed_tests} test(s) ont échoué.")


def main():
    """Point d'entrée principal"""
    try:
        print_header("TEST APPROFONDI DE GOOGLE GEMINI")
        print_info("Modèle: gemini-2.5-flash")
        
        tester = GeminiTranslationTester()
        
        # Exécuter tous les tests
        tester.run_basic_tests()
        tester.run_reverse_tests()
        tester.run_multilang_tests()
        tester.run_long_sentence_tests()
        tester.run_colloquial_tests()
        tester.run_speed_test()
        
        # Afficher le résumé
        tester.print_summary()
        
    except KeyboardInterrupt:
        print_error("\n\nTests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nErreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
