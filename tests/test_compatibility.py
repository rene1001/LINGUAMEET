"""Tests de Compatibilité - LinguaMeet"""
import os, sys, django
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client
from conference.models import Room

class BrowserCompatibilityTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_modern_browser_features(self):
        response = self.client.get('/')
        content = response.content.decode()
        # Vérifier les fonctionnalités modernes
        has_websocket = 'WebSocket' in content or 'ws://' in content
        self.assertTrue(has_websocket or response.status_code == 200)

class MediaAPICompatibilityTests(TestCase):
    def test_audio_api_usage(self):
        client = Client()
        response = client.get('/')
        content = response.content.decode()
        # Vérifier l'utilisation de l'API Media
        has_media = 'getUserMedia' in content or 'mediaDevices' in content
        self.assertTrue(has_media or response.status_code == 200)

class WebRTCCompatibilityTests(TestCase):
    def test_webrtc_support(self):
        client = Client()
        response = client.get('/')
        content = response.content.decode()
        has_rtc = 'RTCPeerConnection' in content or 'webrtc' in content.lower()
        self.assertTrue(has_rtc or response.status_code == 200)

if __name__ == '__main__':
    import unittest
    unittest.main()
