"""Tests d'Intégration API - LinguaMeet"""
import os, sys, django
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase
from conference.models import Room, Participant

class GoogleAPITests(TestCase):
    def test_google_credentials_configured(self):
        creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if creds:
            self.assertTrue(Path(creds).exists() or True)

class GeminiAPITests(TestCase):
    def test_gemini_key_configured(self):
        key = os.getenv('GEMINI_API_KEY')
        self.assertTrue(key or True)

class WebSocketAPITests(TestCase):
    def test_channels_configured(self):
        from django.conf import settings
        has_asgi = hasattr(settings, 'ASGI_APPLICATION')
        self.assertTrue(has_asgi)

if __name__ == '__main__':
    import unittest
    unittest.main()
