"""
Vues pour les pages d'erreur personnalisées
============================================
"""

from django.shortcuts import render


def custom_404(request, exception=None):
    """Page 404 personnalisée"""
    return render(request, '404.html', status=404)


def custom_500(request):
    """Page 500 personnalisée"""
    return render(request, '500.html', status=500)


def offline_view(request):
    """Page hors ligne pour PWA"""
    return render(request, 'offline.html')
