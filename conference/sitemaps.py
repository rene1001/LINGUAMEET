"""
Sitemaps pour LinguaMeet
=========================
Génère automatiquement le sitemap.xml pour le SEO
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Room


class StaticViewSitemap(Sitemap):
    """Sitemap pour les pages statiques"""
    priority = 1.0
    changefreq = 'daily'
    
    def items(self):
        return ['conference:home']
    
    def location(self, item):
        return reverse(item)


class RoomSitemap(Sitemap):
    """Sitemap pour les salles de conférence publiques"""
    changefreq = "hourly"
    priority = 0.8
    
    def items(self):
        # Uniquement les salles actives
        return Room.objects.filter(actif=True).order_by('-date_creation')[:100]
    
    def lastmod(self, obj):
        return obj.date_creation
    
    def location(self, obj):
        return f'/room/{obj.id}/join/'


# Dictionnaire des sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'rooms': RoomSitemap,
}
