#!/usr/bin/env python
"""
Script pour tester l'enregistrement des modèles dans l'admin
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from django.contrib import admin
from conference.models import Room, Participant, ConversationHistory

def test_admin_registration():
    """Tester l'enregistrement des modèles dans l'admin"""
    print("🔍 Test de l'enregistrement des modèles dans l'admin")
    print("=" * 50)
    
    try:
        # Vérifier si les modèles sont enregistrés
        registered_models = admin.site._registry
        
        print(f"📋 Modèles enregistrés dans l'admin: {len(registered_models)}")
        
        for model, admin_class in registered_models.items():
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            admin_name = admin_class.__class__.__name__
            print(f"   ✅ {app_label}.{model_name} -> {admin_name}")
        
        # Vérifier spécifiquement nos modèles
        print(f"\n🎯 Vérification de nos modèles:")
        
        if Room in registered_models:
            print(f"   ✅ Room: {registered_models[Room].__class__.__name__}")
        else:
            print(f"   ❌ Room: NON ENREGISTRÉ")
            
        if Participant in registered_models:
            print(f"   ✅ Participant: {registered_models[Participant].__class__.__name__}")
        else:
            print(f"   ❌ Participant: NON ENREGISTRÉ")
            
        if ConversationHistory in registered_models:
            print(f"   ✅ ConversationHistory: {registered_models[ConversationHistory].__class__.__name__}")
        else:
            print(f"   ❌ ConversationHistory: NON ENREGISTRÉ")
        
        # Vérifier les données existantes
        print(f"\n📊 Données existantes:")
        print(f"   - Salles: {Room.objects.count()}")
        print(f"   - Participants: {Participant.objects.count()}")
        print(f"   - Conversations: {ConversationHistory.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_admin_registration()
    sys.exit(0 if success else 1) 