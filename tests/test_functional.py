"""
Tests Fonctionnels - LinguaMeet
================================
Tests des fonctionnalités principales de l'application
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from conference.models import Room, Participant, ConversationHistory
import json


class RoomFunctionalTests(TestCase):
    """Tests fonctionnels pour les salles de conférence"""
    
    def setUp(self):
        self.client = Client()
    
    def test_create_room(self):
        """Test de création d'une salle"""
        response = self.client.post(reverse('conference:home'), {
            'action': 'create',
            'nom_salle': 'Salle Test',
            'langue_defaut': 'fr'
        })
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertTrue(Room.objects.filter(nom='Salle Test').exists())
    
    def test_join_room(self):
        """Test de rejoindre une salle"""
        room = Room.objects.create(nom='Test Room', langue_par_defaut='fr')
        response = self.client.get(reverse('conference:join_room', args=[room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Room')
    
    def test_room_with_invalid_id(self):
        """Test d'accès à une salle invalide"""
        response = self.client.get(reverse('conference:join_room', args=['invalid-uuid']))
        self.assertEqual(response.status_code, 404)
    
    def test_inactive_room(self):
        """Test d'accès à une salle inactive"""
        room = Room.objects.create(nom='Inactive Room', actif=False)
        response = self.client.get(reverse('conference:join_room', args=[room.id]))
        self.assertEqual(response.status_code, 404)


class ParticipantFunctionalTests(TestCase):
    """Tests fonctionnels pour les participants"""
    
    def setUp(self):
        self.client = Client()
        self.room = Room.objects.create(nom='Test Room', langue_par_defaut='fr')
    
    def test_create_participant(self):
        """Test de création d'un participant"""
        response = self.client.post(reverse('conference:join_room', args=[self.room.id]), {
            'nom_participant': 'Alice',
            'langue_parole': 'fr',
            'langue_souhaitée': 'en'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Participant.objects.filter(nom='Alice').exists())
    
    def test_participant_language_settings(self):
        """Test des paramètres de langue du participant"""
        participant = Participant.objects.create(
            nom='Bob',
            langue_parole='en',
            langue_souhaitée='fr',
            room=self.room
        )
        self.assertEqual(participant.langue_parole, 'en')
        self.assertEqual(participant.langue_souhaitée, 'fr')
    
    def test_participant_status(self):
        """Test du statut du participant"""
        participant = Participant.objects.create(
            nom='Charlie',
            room=self.room,
            actif=True,
            micro_actif=True
        )
        self.assertTrue(participant.actif)
        self.assertTrue(participant.micro_actif)


class ConversationFunctionalTests(TestCase):
    """Tests fonctionnels pour les conversations"""
    
    def setUp(self):
        self.room = Room.objects.create(nom='Test Room')
        self.speaker = Participant.objects.create(
            nom='Speaker',
            langue_parole='fr',
            langue_souhaitée='en',
            room=self.room
        )
        self.listener = Participant.objects.create(
            nom='Listener',
            langue_parole='en',
            langue_souhaitée='fr',
            room=self.room
        )
    
    def test_create_conversation_history(self):
        """Test de création d'historique de conversation"""
        conversation = ConversationHistory.objects.create(
            room=self.room,
            speaker=self.speaker,
            listener=self.listener,
            original_text="Bonjour",
            translated_text="Hello",
            original_language="fr",
            target_language="en"
        )
        self.assertIsNotNone(conversation.id)
        self.assertEqual(conversation.original_text, "Bonjour")
        self.assertEqual(conversation.translated_text, "Hello")
    
    def test_conversation_history_ordering(self):
        """Test du tri de l'historique"""
        conv1 = ConversationHistory.objects.create(
            room=self.room,
            speaker=self.speaker,
            listener=self.listener,
            original_text="Premier",
            translated_text="First",
            original_language="fr",
            target_language="en"
        )
        conv2 = ConversationHistory.objects.create(
            room=self.room,
            speaker=self.speaker,
            listener=self.listener,
            original_text="Deuxième",
            translated_text="Second",
            original_language="fr",
            target_language="en"
        )
        conversations = ConversationHistory.objects.all()
        self.assertEqual(conversations[0].id, conv2.id)  # Plus récent en premier


class NavigationFunctionalTests(TestCase):
    """Tests de navigation dans l'application"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page_loads(self):
        """Test de chargement de la page d'accueil"""
        response = self.client.get(reverse('conference:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LinguaMeet')
    
    def test_leave_room(self):
        """Test de quitter une salle"""
        room = Room.objects.create(nom='Test Room')
        participant = Participant.objects.create(
            nom='Test User',
            room=room
        )
        session = self.client.session
        session['participant_id'] = str(participant.id)
        session.save()
        
        response = self.client.get(reverse('conference:leave_room', args=[room.id]))
        self.assertEqual(response.status_code, 302)


class WebSocketFunctionalTests(TestCase):
    """Tests fonctionnels pour les WebSockets"""
    
    def test_websocket_url_configuration(self):
        """Test de la configuration des URLs WebSocket"""
        from linguameet_project import routing
        self.assertTrue(hasattr(routing, 'websocket_urlpatterns'))
        self.assertGreater(len(routing.websocket_urlpatterns), 0)


class LanguageSupportTests(TestCase):
    """Tests de support des langues"""
    
    def test_supported_languages_exist(self):
        """Test de la présence des langues supportées"""
        from django.conf import settings
        self.assertIn('SUPPORTED_LANGUAGES', dir(settings))
        supported = settings.SUPPORTED_LANGUAGES
        self.assertIn('fr', supported)
        self.assertIn('en', supported)
        self.assertIn('es', supported)
    
    def test_language_display_names(self):
        """Test des noms d'affichage des langues"""
        room = Room.objects.create(nom='Test', langue_par_defaut='fr')
        self.assertIsNotNone(room.langue_par_defaut_display)


if __name__ == '__main__':
    import unittest
    unittest.main()
