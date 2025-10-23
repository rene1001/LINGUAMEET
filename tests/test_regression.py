"""Tests de Régression - LinguaMeet"""
import os, sys, django
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client
from conference.models import Room, Participant

class CoreFunctionalityRegressionTests(TestCase):
    def test_room_creation_still_works(self):
        room = Room.objects.create(nom='Regression Test', langue_par_defaut='fr')
        self.assertIsNotNone(room.id)
    
    def test_participant_creation_still_works(self):
        room = Room.objects.create(nom='Test')
        participant = Participant.objects.create(
            nom='Test User',
            room=room,
            langue_parole='fr',
            langue_souhaitée='en'
        )
        self.assertIsNotNone(participant.id)

class URLRegressionTests(TestCase):
    def test_home_url_unchanged(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    import unittest
    unittest.main()
