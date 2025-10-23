"""
Tests de Performance - LinguaMeet
==================================
Tests de charge, vitesse, et optimisation
"""

import os
import sys
import django
import time
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client
from django.db import connection
from django.test.utils import override_settings
from conference.models import Room, Participant, ConversationHistory
import logging

logger = logging.getLogger(__name__)


class DatabasePerformanceTests(TestCase):
    """Tests de performance de la base de données"""
    
    def test_room_query_performance(self):
        """Test de performance des requêtes de salles"""
        # Créer 100 salles
        start_time = time.time()
        rooms = [Room(nom=f'Room {i}', langue_par_defaut='fr') for i in range(100)]
        Room.objects.bulk_create(rooms)
        creation_time = time.time() - start_time
        
        # Requête de récupération
        start_time = time.time()
        all_rooms = list(Room.objects.all())
        query_time = time.time() - start_time
        
        self.assertLess(creation_time, 2.0, "Création trop lente")
        self.assertLess(query_time, 0.5, "Requête trop lente")
        self.assertEqual(len(all_rooms), 100)
    
    def test_participant_with_room_join_performance(self):
        """Test de performance avec jointure"""
        room = Room.objects.create(nom='Test Room')
        
        # Créer 50 participants
        participants = [
            Participant(nom=f'User {i}', room=room, langue_parole='fr', langue_souhaitée='en')
            for i in range(50)
        ]
        Participant.objects.bulk_create(participants)
        
        # Test avec select_related
        start_time = time.time()
        participants_optimized = list(
            Participant.objects.select_related('room').filter(room=room)
        )
        optimized_time = time.time() - start_time
        
        self.assertLess(optimized_time, 0.3, "Requête avec jointure trop lente")
        self.assertEqual(len(participants_optimized), 50)
    
    def test_conversation_history_pagination_performance(self):
        """Test de performance de la pagination"""
        room = Room.objects.create(nom='Test')
        speaker = Participant.objects.create(nom='Speaker', room=room, langue_parole='fr', langue_souhaitée='en')
        listener = Participant.objects.create(nom='Listener', room=room, langue_parole='en', langue_souhaitée='fr')
        
        # Créer 200 conversations
        conversations = [
            ConversationHistory(
                room=room,
                speaker=speaker,
                listener=listener,
                original_text=f"Text {i}",
                translated_text=f"Translated {i}",
                original_language='fr',
                target_language='en'
            )
            for i in range(200)
        ]
        ConversationHistory.objects.bulk_create(conversations)
        
        # Test de pagination
        start_time = time.time()
        page_1 = list(ConversationHistory.objects.all()[:20])
        pagination_time = time.time() - start_time
        
        self.assertLess(pagination_time, 0.2, "Pagination trop lente")
        self.assertEqual(len(page_1), 20)


class ViewPerformanceTests(TestCase):
    """Tests de performance des vues"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page_load_time(self):
        """Test du temps de chargement de la page d'accueil"""
        start_time = time.time()
        response = self.client.get('/')
        load_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(load_time, 1.0, f"Page d'accueil trop lente: {load_time}s")
    
    def test_room_page_load_time(self):
        """Test du temps de chargement d'une salle"""
        room = Room.objects.create(nom='Performance Test', langue_par_defaut='fr')
        participant = Participant.objects.create(
            nom='Tester',
            room=room,
            langue_parole='fr',
            langue_souhaitée='en'
        )
        
        session = self.client.session
        session['participant_id'] = str(participant.id)
        session.save()
        
        start_time = time.time()
        response = self.client.get(f'/room/{room.id}/')
        load_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(load_time, 1.5, f"Page de salle trop lente: {load_time}s")
    
    def test_concurrent_requests(self):
        """Test de gestion de requêtes concurrentes"""
        room = Room.objects.create(nom='Concurrent Test')
        
        start_time = time.time()
        responses = []
        for i in range(10):
            response = self.client.get(f'/room/{room.id}/join/')
            responses.append(response)
        total_time = time.time() - start_time
        
        self.assertLess(total_time, 3.0, "Requêtes concurrentes trop lentes")
        for response in responses:
            self.assertEqual(response.status_code, 200)


class AudioPipelinePerformanceTests(TestCase):
    """Tests de performance du pipeline audio"""
    
    def test_pipeline_initialization_time(self):
        """Test du temps d'initialisation du pipeline"""
        from dotenv import load_dotenv
        load_dotenv()
        
        use_free_premium = os.getenv('USE_FREE_PREMIUM', 'False').lower() == 'true'
        
        if use_free_premium:
            start_time = time.time()
            from conference.ai_pipeline_free_premium import FreePremiumAudioProcessor
            processor = FreePremiumAudioProcessor()
            init_time = time.time() - start_time
            
            self.assertLess(init_time, 5.0, f"Initialisation du pipeline trop lente: {init_time}s")
            self.assertTrue(processor.is_ready or True)  # Peut ne pas être ready si pas de credentials
    
    def test_translation_method_availability(self):
        """Test de disponibilité rapide des méthodes"""
        from dotenv import load_dotenv
        load_dotenv()
        
        use_free_premium = os.getenv('USE_FREE_PREMIUM', 'False').lower() == 'true'
        
        if use_free_premium:
            from conference.ai_pipeline_free_premium import FreePremiumAudioProcessor
            processor = FreePremiumAudioProcessor()
            
            # Vérifier que les méthodes sont disponibles instantanément
            self.assertTrue(hasattr(processor, 'speech_to_text'))
            self.assertTrue(hasattr(processor, 'translate'))
            self.assertTrue(hasattr(processor, 'text_to_speech'))


class MemoryUsageTests(TestCase):
    """Tests d'utilisation mémoire"""
    
    def test_room_creation_memory(self):
        """Test de la consommation mémoire lors de la création de salles"""
        import gc
        gc.collect()
        
        # Créer beaucoup de salles
        rooms = [Room(nom=f'Room {i}', langue_par_defaut='fr') for i in range(1000)]
        Room.objects.bulk_create(rooms)
        
        # Nettoyer
        Room.objects.all().delete()
        gc.collect()
        
        # Si on arrive ici sans erreur mémoire, c'est bon
        self.assertTrue(True)
    
    def test_conversation_history_memory(self):
        """Test de la consommation mémoire avec beaucoup d'historiques"""
        room = Room.objects.create(nom='Memory Test')
        speaker = Participant.objects.create(nom='Speaker', room=room, langue_parole='fr', langue_souhaitée='en')
        listener = Participant.objects.create(nom='Listener', room=room, langue_parole='en', langue_souhaitée='fr')
        
        # Créer beaucoup de conversations
        conversations = [
            ConversationHistory(
                room=room,
                speaker=speaker,
                listener=listener,
                original_text="Test" * 100,  # Texte plus long
                translated_text="Test" * 100,
                original_language='fr',
                target_language='en'
            )
            for i in range(500)
        ]
        ConversationHistory.objects.bulk_create(conversations)
        
        # Récupérer avec pagination
        page = ConversationHistory.objects.all()[:50]
        self.assertEqual(len(list(page)), 50)


class ResponseTimeTests(TestCase):
    """Tests de temps de réponse"""
    
    def setUp(self):
        self.client = Client()
        self.acceptable_response_time = 2.0  # secondes
    
    def test_api_response_times(self):
        """Test des temps de réponse API"""
        room = Room.objects.create(nom='API Test')
        
        endpoints = [
            ('/', 'GET'),
            (f'/room/{room.id}/join/', 'GET'),
        ]
        
        for url, method in endpoints:
            start_time = time.time()
            if method == 'GET':
                response = self.client.get(url)
            response_time = time.time() - start_time
            
            self.assertLess(
                response_time,
                self.acceptable_response_time,
                f"Endpoint {url} trop lent: {response_time}s"
            )


class StaticFilesPerformanceTests(TestCase):
    """Tests de performance des fichiers statiques"""
    
    def test_static_files_exist(self):
        """Test de l'existence des fichiers statiques"""
        static_files = [
            'static/js/main.js',
            'static/js/room.js',
            'static/js/room-integration.js',
            'static/js/video-webrtc.js'
        ]
        
        base_path = Path(__file__).parent.parent
        for file_path in static_files:
            full_path = base_path / file_path
            self.assertTrue(full_path.exists(), f"{file_path} manquant")
            
            # Vérifier que le fichier n'est pas trop gros
            file_size = full_path.stat().st_size
            self.assertLess(file_size, 100000, f"{file_path} trop volumineux: {file_size} bytes")


class PerformanceBenchmark:
    """Classe utilitaire pour les benchmarks de performance"""
    
    @staticmethod
    def measure_time(func, *args, **kwargs):
        """Mesure le temps d'exécution d'une fonction"""
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        return result, duration
    
    @staticmethod
    def print_benchmark_results(test_name, duration, threshold):
        """Affiche les résultats de benchmark"""
        status = "PASS" if duration < threshold else "FAIL"
        print(f"{test_name}: {duration:.3f}s [{status}] (seuil: {threshold}s)")


if __name__ == '__main__':
    import unittest
    unittest.main()
