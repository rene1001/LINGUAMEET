#!/usr/bin/env python
"""
Script pour créer un superutilisateur admin
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Créer un superutilisateur admin"""
    try:
        # Vérifier si l'utilisateur admin existe déjà
        if User.objects.filter(username='admin').exists():
            print("✅ L'utilisateur admin existe déjà")
            return True
        
        # Créer le superutilisateur
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@linguameet.com',
            password='admin123'
        )
        
        print("✅ Superutilisateur créé avec succès!")
        print(f"   Username: admin")
        print(f"   Email: admin@linguameet.com")
        print(f"   Password: admin123")
        print(f"   ID: {admin_user.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

if __name__ == "__main__":
    success = create_admin_user()
    if success:
        print("\n🌐 Accédez à l'admin: http://localhost:8000/admin/")
        print("   Connectez-vous avec admin/admin123")
    sys.exit(0 if success else 1) 