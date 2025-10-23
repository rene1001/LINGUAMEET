"""
Vues SEO pour LinguaMeet
========================
Vues pour robots.txt et autres fichiers SEO
"""

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from pathlib import Path


@require_GET
def robots_txt(request):
    """Servir le fichier robots.txt"""
    robots_path = Path(__file__).resolve().parent.parent / 'static' / 'robots.txt'
    
    try:
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer localhost par le domaine réel si en production
        if not request.get_host().startswith('localhost'):
            content = content.replace('http://localhost:8000', f'{request.scheme}://{request.get_host()}')
        
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        # Fallback si le fichier n'existe pas
        content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: {scheme}://{host}/sitemap.xml
""".format(scheme=request.scheme, host=request.get_host())
        
        return HttpResponse(content, content_type='text/plain')
