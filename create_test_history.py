#!/usr/bin/env python
"""
Script pour créer des données de test dans l'historique des conversations
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguameet_project.settings')
django.setup()

from conference.models import Room, Participant, ConversationHistory
from conference.ai_pipeline import AudioProcessor
from django.core.files.base import ContentFile

def create_test_history():
    """Créer des données de test pour l'historique"""
    print("📝 Création de données de test pour l'historique")
    print("=" * 50)
    
    try:
        # Créer une salle de test
        room = Room.objects.create(
            nom="Salle de conférence internationale",
            actif=True
        )
        print(f"✅ Salle créée: {room.nom}")
        
        # Créer plusieurs participants
        participants = [
            Participant.objects.create(
                room=room,
                nom="Marie (Français)",
                langue_parole="fr",
                langue_souhaitée="en",
                actif=True,
                micro_actif=True
            ),
            Participant.objects.create(
                room=room,
                nom="John (Anglais)",
                langue_parole="en",
                langue_souhaitée="fr",
                actif=True,
                micro_actif=True
            ),
            Participant.objects.create(
                room=room,
                nom="Carlos (Espagnol)",
                langue_parole="es",
                langue_souhaitée="fr",
                actif=True,
                micro_actif=True
            ),
            Participant.objects.create(
                room=room,
                nom="Anna (Allemand)",
                langue_parole="de",
                langue_souhaitée="en",
                actif=True,
                micro_actif=True
            )
        ]
        
        print(f"✅ Participants créés: {len(participants)}")
        
        # Initialiser le pipeline audio
        audio_processor = AudioProcessor()
        
        # Conversations de test avec différents timestamps
        test_conversations = [
            # Conversations récentes (aujourd'hui)
            ("Bonjour tout le monde, comment allez-vous ?", "fr", "en", 0),
            ("Hello everyone, how are you doing?", "en", "fr", 0),
            ("Je suis ravi de participer à cette conférence.", "fr", "en", 0),
            ("I am excited to participate in this conference.", "en", "fr", 0),
            ("¿Cómo están todos?", "es", "fr", 0),
            ("Wie geht es euch allen?", "de", "en", 0),
            
            # Conversations d'hier
            ("Nous avons beaucoup de travail à faire.", "fr", "en", 1),
            ("We have a lot of work to do.", "en", "fr", 1),
            ("¿Cuál es el próximo paso?", "es", "fr", 1),
            ("Was ist der nächste Schritt?", "de", "en", 1),
            
            # Conversations de la semaine dernière
            ("La réunion était très productive.", "fr", "en", 7),
            ("The meeting was very productive.", "en", "fr", 7),
            ("¿Cuándo es la próxima reunión?", "es", "fr", 7),
            ("Wann ist das nächste Treffen?", "de", "en", 7),
            
            # Conversations plus anciennes
            ("Merci pour votre participation.", "fr", "en", 14),
            ("Thank you for your participation.", "en", "fr", 14),
            ("¿Tienen alguna pregunta?", "es", "fr", 14),
            ("Haben Sie Fragen?", "de", "en", 14),
        ]
        
        conversations_created = 0
        
        for original_text, original_lang, target_lang, days_ago in test_conversations:
            print(f"\n🎤 Création conversation: '{original_text}' ({original_lang} → {target_lang})")
            
            # Traduire le texte
            translated_text = audio_processor.translate_sync(original_text, original_lang, target_lang)
            
            # Générer l'audio
            audio_bytes = audio_processor.text_to_speech_sync(translated_text, target_lang)
            
            if audio_bytes:
                # Créer des conversations pour différents participants
                for speaker in participants:
                    for listener in participants:
                        # Ne pas créer de conversation pour le même participant
                        if speaker.id == listener.id:
                            continue
                        
                        # Créer l'enregistrement avec timestamp personnalisé
                        timestamp = datetime.now() - timedelta(days=days_ago)
                        
                        conversation = ConversationHistory.objects.create(
                            room=room,
                            speaker=speaker,
                            listener=listener,
                            original_text=original_text,
                            translated_text=translated_text,
                            original_language=original_lang,
                            target_language=listener.langue_souhaitée,
                            audio_duration=len(audio_bytes) / 16000,
                            timestamp=timestamp
                        )
                        
                        # Sauvegarder le fichier audio
                        filename = f"history_test_{conversation.id}_{speaker.nom}_{listener.nom}.wav"
                        conversation.audio_file.save(
                            filename,
                            ContentFile(audio_bytes),
                            save=True
                        )
                        
                        conversations_created += 1
                        
                        if conversations_created <= 5:  # Afficher seulement les 5 premières
                            print(f"   💾 {speaker.nom} → {listener.nom}: {conversation.id}")
        
        print(f"\n📊 Résumé:")
        print(f"   - Conversations créées: {conversations_created}")
        print(f"   - Fichiers audio sauvegardés: {conversations_created}")
        print(f"   - Participants: {len(participants)}")
        print(f"   - Période: {test_conversations[-1][3]} jours")
        
        # Afficher quelques exemples
        print(f"\n📋 Exemples de conversations:")
        recent_conversations = ConversationHistory.objects.filter(room=room).order_by('-timestamp')[:5]
        for conv in recent_conversations:
            print(f"   - {conv.speaker.nom} → {conv.listener.nom}")
            print(f"     '{conv.original_text}' → '{conv.translated_text}'")
            print(f"     📅 {conv.timestamp.strftime('%d/%m/%Y %H:%M')}")
            print(f"     📁 {conv.audio_file.name}")
            print()
        
        print("✅ Données de test créées avec succès!")
        print(f"🌐 Accédez à l'historique: http://localhost:8000/conversation-history/")
        
        return room.id
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    room_id = create_test_history()
    if room_id:
        print(f"🎯 ID de la salle créée: {room_id}")
    sys.exit(0 if room_id else 1) 