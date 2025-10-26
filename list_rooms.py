#!/usr/bin/env python
"""
Script pour lister toutes les salles
Usage: python list_rooms.py
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from conference.models import Room

# Lister toutes les salles
rooms = Room.objects.all()

print(f"📊 Nombre de salles : {rooms.count()}\n")

if rooms.count() == 0:
    print("❌ Aucune salle trouvée.")
    print("   Créez-en une avec: python create_test_room.py")
else:
    print("Salles disponibles :")
    print("=" * 80)
    for room in rooms:
        status = "🟢 Active" if room.actif else "🔴 Inactive"
        print(f"\n{status}")
        print(f"  Nom: {room.nom}")
        print(f"  ID: {room.id}")
        print(f"  Langue: {room.langue_par_defaut}")
        print(f"  Créée le: {room.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  URL: http://localhost:10000/room/{room.id}/")
        print(f"  Participants: {room.participants.filter(actif=True).count()}")
