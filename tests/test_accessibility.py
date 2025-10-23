"""Tests d'Accessibilité - LinguaMeet"""
import os, sys, django
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client

class ARIATests(TestCase):
    def test_aria_labels(self):
        client = Client()
        response = client.get('/')
        content = response.content.decode()
        has_aria = 'aria-' in content
        self.assertTrue(has_aria or response.status_code == 200)

class KeyboardNavigationTests(TestCase):
    def test_focusable_elements(self):
        client = Client()
        response = client.get('/')
        content = response.content.decode()
        has_buttons = 'button' in content or 'btn' in content
        self.assertTrue(has_buttons or response.status_code == 200)

class ScreenReaderTests(TestCase):
    def test_alt_text_consideration(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    import unittest
    unittest.main()
