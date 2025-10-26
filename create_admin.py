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
        # Récupérer les credentials depuis les variables d'environnement ou utiliser les valeurs par défaut
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@linguameet.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        # Vérifier si l'utilisateur admin existe déjà
        if User.objects.filter(username=admin_username).exists():
            print(f"✅ L'utilisateur '{admin_username}' existe déjà")
            admin_user = User.objects.get(username=admin_username)
            
            # Mettre à jour le mot de passe si fourni en variable d'environnement
            if os.getenv('ADMIN_PASSWORD'):
                admin_user.set_password(admin_password)
                admin_user.save()
                print(f"🔄 Mot de passe mis à jour pour '{admin_username}'")
            
            return True
        
        # Créer le superutilisateur
        admin_user = User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        
        print("✅ Superutilisateur créé avec succès!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Password: {'*' * len(admin_password)} (masqué)")
        print(f"   ID: {admin_user.id}")
        print("\n⚠️  IMPORTANT: Changez ce mot de passe après la première connexion!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_admin_user()
    if success:
        print("\n🌐 Accédez à l'admin: http://localhost:8000/admin/ (ou votre domaine)")
    sys.exit(0 if success else 1) 