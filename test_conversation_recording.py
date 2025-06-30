#!/usr/bin/env python
"""
Script de test pour l'enregistrement automatique des conversations
"""

import os
import sys
import django
import json
import base64
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from conference.models import Room, Participant, ConversationHistory
from conference.ai_pipeline import AudioProcessor
from django.core.files.base import ContentFile

def test_conversation_recording():
    """Test de l'enregistrement automatique des conversations"""
    print("🧪 Test de l'enregistrement automatique des conversations")
    print("=" * 60)
    
    try:
        # Créer une salle de test
        room = Room.objects.create(
            nom="Salle de test enregistrement",
            actif=True
        )
        print(f"✅ Salle créée: {room.nom}")
        
        # Créer deux participants
        participant1 = Participant.objects.create(
            room=room,
            nom="Alice (Français)",
            langue_parole="fr",
            langue_souhaitée="en",
            actif=True,
            micro_actif=True
        )
        
        participant2 = Participant.objects.create(
            room=room,
            nom="Bob (Anglais)",
            langue_parole="en",
            langue_souhaitée="fr",
            actif=True,
            micro_actif=True
        )
        
        print(f"✅ Participants créés: {participant1.nom} et {participant2.nom}")
        
        # Initialiser le pipeline audio
        audio_processor = AudioProcessor()
        
        # Texte de test
        test_texts = [
            ("Bonjour, comment allez-vous ?", "fr"),
            ("Hello, how are you?", "en"),
            ("Je suis ravi de vous rencontrer.", "fr"),
            ("I am happy to meet you.", "en")
        ]
        
        conversations_created = 0
        
        for original_text, original_lang in test_texts:
            print(f"\n🎤 Test avec: '{original_text}' ({original_lang})")
            
            # Simuler la traduction
            if original_lang == "fr":
                translated_text = audio_processor.translate_sync(original_text, "fr", "en")
                target_lang = "en"
            else:
                translated_text = audio_processor.translate_sync(original_text, "en", "fr")
                target_lang = "fr"
            
            print(f"   Traduit: '{translated_text}' ({target_lang})")
            
            # Simuler la synthèse vocale
            audio_bytes = audio_processor.text_to_speech_sync(translated_text, target_lang)
            
            if audio_bytes:
                print(f"   ✅ Audio généré: {len(audio_bytes)} bytes")
                
                # Créer l'enregistrement de conversation pour chaque participant
                for listener in [participant1, participant2]:
                    # Ne pas créer d'enregistrement pour l'émetteur lui-même
                    if listener.id == participant1.id and original_lang == "fr":
                        speaker = participant1
                    elif listener.id == participant2.id and original_lang == "en":
                        speaker = participant2
                    else:
                        continue
                    
                    # Créer l'enregistrement
                    conversation = ConversationHistory.objects.create(
                        room=room,
                        speaker=speaker,
                        listener=listener,
                        original_text=original_text,
                        translated_text=translated_text,
                        original_language=original_lang,
                        target_language=listener.langue_souhaitée,
                        audio_duration=len(audio_bytes) / 16000  # Estimation
                    )
                    
                    # Sauvegarder le fichier audio
                    filename = f"test_conversation_{conversation.id}_{speaker.nom}_{listener.nom}.wav"
                    conversation.audio_file.save(
                        filename,
                        ContentFile(audio_bytes),
                        save=True
                    )
                    
                    conversations_created += 1
                    print(f"   💾 Conversation sauvegardée: {conversation.id}")
                    print(f"   📁 Fichier audio: {conversation.audio_file.name}")
        
        print(f"\n📊 Résumé:")
        print(f"   - Conversations créées: {conversations_created}")
        print(f"   - Fichiers audio sauvegardés: {conversations_created}")
        
        # Vérifier les enregistrements dans la base de données
        total_conversations = ConversationHistory.objects.filter(room=room).count()
        print(f"   - Total en base: {total_conversations}")
        
        # Lister les conversations
        print(f"\n📋 Conversations enregistrées:")
        conversations = ConversationHistory.objects.filter(room=room).order_by('timestamp')
        for conv in conversations:
            print(f"   - {conv.speaker.nom} → {conv.listener.nom}: '{conv.original_text}' → '{conv.translated_text}'")
            if conv.audio_file:
                print(f"     📁 Audio: {conv.audio_file.name} ({conv.audio_duration:.2f}s)")
        
        # Nettoyer les données de test
        print(f"\n🧹 Nettoyage des données de test...")
        room.delete()  # Cela supprimera aussi les participants et conversations
        
        print("✅ Test terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_conversation_recording()
    sys.exit(0 if success else 1) 