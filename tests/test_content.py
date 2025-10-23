"""Tests de Contenu - LinguaMeet"""
import os, sys, django
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client

class ContentQualityTests(TestCase):
    def test_homepage_content(self):
        client = Client()
        response = client.get('/')
        self.assertContains(response, 'LinguaMeet' or 'Conference' or 'Traduction')
    
    def test_error_messages_friendly(self):
        client = Client()
        response = client.get('/room/invalid-uuid/')
        self.assertEqual(response.status_code, 404)

class LanguageSupportTests(TestCase):
    def test_multiple_languages_supported(self):
        from django.conf import settings
        langs = settings.SUPPORTED_LANGUAGES
        self.assertGreaterEqual(len(langs), 5)

if __name__ == '__main__':
    import unittest
    unittest.main()
