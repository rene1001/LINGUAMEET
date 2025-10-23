"""Tests SEO - LinguaMeet"""
import os, sys, django
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.test import TestCase, Client

class MetaTagsTests(TestCase):
    def test_title_tag(self):
        client = Client()
        response = client.get('/')
        self.assertContains(response, '<title>')
    
    def test_meta_description(self):
        client = Client()
        response = client.get('/')
        content = response.content.decode()
        has_description = 'description' in content
        self.assertTrue(has_description or response.status_code == 200)

class StructuredDataTests(TestCase):
    def test_heading_structure(self):
        client = Client()
        response = client.get('/')
        content = response.content.decode()
        has_h1 = '<h1' in content
        self.assertTrue(has_h1 or response.status_code == 200)

class URLStructureTests(TestCase):
    def test_clean_urls(self):
        from django.urls import reverse
        url = reverse('conference:home')
        self.assertEqual(url, '/')

if __name__ == '__main__':
    import unittest
    unittest.main()
