#!/usr/bin/env python
"""
Script pour créer une salle de test
Usage: python create_test_room.py
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from conference.models import Room

# Créer une salle de test
room = Room.objects.create(
    nom="Salle de Test",
    langue_par_defaut="fr"
)

print(f"✅ Salle créée avec succès !")
print(f"   ID: {room.id}")
print(f"   Nom: {room.nom}")
print(f"   URL: http://localhost:10000/room/{room.id}/")
print(f"\n🔗 Accédez à la salle:")
print(f"   http://localhost:10000/room/{room.id}/")
