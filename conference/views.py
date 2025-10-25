from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
import json
import uuid
import os
from .models import Room, Participant, ConversationHistory
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


def home(request):
    """Page d'accueil pour créer ou rejoindre une réunion"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            nom_salle = request.POST.get('nom_salle', 'Nouvelle réunion')
            langue_defaut = request.POST.get('langue_defaut', 'fr')
            
            room = Room.objects.create(
                nom=nom_salle,
                langue_par_defaut=langue_defaut
            )
            
            return redirect('conference:join_room', room_id=room.id)
            
        elif action == 'join':
            room_id = request.POST.get('room_id')
            try:
                room = Room.objects.get(id=room_id, actif=True)
                return redirect('conference:join_room', room_id=room.id)
            except (Room.DoesNotExist, ValueError, ValidationError):
                messages.error(request, "Salle introuvable ou inactive.")
    
    return render(request, 'conference/home.html', {
        'supported_languages': settings.SUPPORTED_LANGUAGES
    })


def join_room(request, room_id):
    """Page pour rejoindre une salle de conférence"""
    room = get_object_or_404(Room, id=room_id, actif=True)
    
    if request.method == 'POST':
        nom_participant = request.POST.get('nom_participant')
        langue_souhaitée = request.POST.get('langue_souhaitée', 'en')
        langue_parole = request.POST.get('langue_parole', 'fr')
        
        if nom_participant:
            # Créer le participant
            participant = Participant.objects.create(
                nom=nom_participant,
                langue_souhaitée=langue_souhaitée,
                langue_parole=langue_parole,
                room=room,
                session_id=request.session.session_key or str(uuid.uuid4())
            )
            
            # Stocker l'ID du participant en session
            request.session['participant_id'] = str(participant.id)
            request.session['room_id'] = str(room.id)
            
            return redirect('conference:room', room_id=room.id)
    
    return render(request, 'conference/join_room.html', {
        'room': room,
        'supported_languages': settings.SUPPORTED_LANGUAGES
    })


def room(request, room_id):
    """Page de la salle de conférence"""
    room = get_object_or_404(Room, id=room_id, actif=True)
    participant_id = request.session.get('participant_id')
    
    if not participant_id:
        # Rediriger vers la sélection de langue
        return redirect('conference:select_language', room_id=room_id)
    
    try:
        participant = Participant.objects.get(id=participant_id, room=room, actif=True)
    except (Participant.DoesNotExist, ValueError, ValidationError):
        # Rediriger vers la sélection de langue
        return redirect('conference:select_language', room_id=room_id)
    
    participants = room.participants.filter(actif=True).exclude(id=participant.id)
    
    return render(request, 'conference/room.html', {
        'room': room,
        'participant': participant,
        'participants': participants,
        'supported_languages': settings.SUPPORTED_LANGUAGES
    })


@csrf_exempt
@require_http_methods(["POST"])
def update_participant(request, room_id):
    """API pour mettre à jour les informations d'un participant"""
    try:
        data = json.loads(request.body)
        participant_id = request.session.get('participant_id')
        
        if not participant_id:
            return JsonResponse({'error': 'Participant non trouvé'}, status=400)
        
        participant = Participant.objects.get(id=participant_id, room_id=room_id)
        
        if 'micro_actif' in data:
            participant.micro_actif = data['micro_actif']
        
        if 'langue' in data:
            # Compatibilité: le client envoie 'langue' -> map sur langue_parole
            participant.langue_parole = data['langue']
        
        participant.save()
        
        return JsonResponse({'success': True})
        
    except (Participant.DoesNotExist, ValueError, ValidationError) as e:
        return JsonResponse({'error': 'Participant invalide'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def leave_room(request, room_id):
    """Quitter une salle de conférence"""
    participant_id = request.session.get('participant_id')
    
    if participant_id:
        try:
            participant = Participant.objects.get(id=participant_id, room_id=room_id)
            participant.actif = False
            participant.save()
        except (Participant.DoesNotExist, ValueError, ValidationError):
            pass
    
    # Nettoyer la session
    if 'participant_id' in request.session:
        del request.session['participant_id']
    if 'room_id' in request.session:
        del request.session['room_id']
    
    messages.success(request, "Vous avez quitté la salle de conférence.")
    return redirect('conference:home')


def conversation_history(request, room_id):
    """Page d'historique des conversations"""
    room = get_object_or_404(Room, id=room_id, actif=True)
    participant_id = request.session.get('participant_id')
    
    if not participant_id:
        return redirect('conference:join_room', room_id=room_id)
    
    try:
        participant = Participant.objects.get(id=participant_id, room=room, actif=True)
    except (Participant.DoesNotExist, ValueError, ValidationError):
        return redirect('conference:join_room', room_id=room_id)
    
    # Récupérer l'historique des conversations de ce participant
    conversations = ConversationHistory.objects.filter(
        Q(speaker=participant) | Q(listener=participant),
        room=room
    ).order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(conversations, 20)  # 20 conversations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'conference/conversation_history.html', {
        'room': room,
        'participant': participant,
        'conversations': page_obj,
        'supported_languages': settings.SUPPORTED_LANGUAGES
    })


@csrf_exempt
@require_http_methods(["POST"])
def save_conversation(request, room_id):
    """API pour sauvegarder une conversation"""
    try:
        data = json.loads(request.body)
        participant_id = request.session.get('participant_id')
        
        if not participant_id:
            return JsonResponse({'error': 'Participant non trouvé'}, status=400)
        
        # Récupérer les participants
        speaker = Participant.objects.get(id=data.get('speaker_id'))
        listener = Participant.objects.get(id=participant_id)
        room = Room.objects.get(id=room_id)
        
        # Créer l'enregistrement de conversation
        conversation = ConversationHistory.objects.create(
            room=room,
            speaker=speaker,
            listener=listener,
            original_text=data.get('original_text', ''),
            translated_text=data.get('translated_text', ''),
            original_language=data.get('original_language', 'fr'),
            target_language=data.get('target_language', 'en'),
            audio_duration=data.get('audio_duration', 0.0)
        )
        
        # Sauvegarder le fichier audio si fourni
        if 'audio_data' in data:
            import base64
            audio_bytes = base64.b64decode(data['audio_data'])
            
            # Créer le nom de fichier
            filename = f"conversation_{conversation.id}.wav"
            file_path = os.path.join(settings.MEDIA_ROOT, 'conversations', filename)
            
            # Créer le dossier si nécessaire
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Sauvegarder le fichier
            with open(file_path, 'wb') as f:
                f.write(audio_bytes)
            
            conversation.audio_file = f'conversations/{filename}'
            conversation.save()
        
        return JsonResponse({
            'success': True,
            'conversation_id': str(conversation.id)
        })
        
    except (Participant.DoesNotExist, Room.DoesNotExist, ValueError, ValidationError):
        return JsonResponse({'error': 'Participant ou salle invalide'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def download_audio(request, conversation_id):
    """Télécharger un fichier audio de conversation"""
    conversation = get_object_or_404(ConversationHistory, id=conversation_id)
    participant_id = request.session.get('participant_id')
    
    # Vérifier que l'utilisateur a accès à cette conversation
    if not participant_id or (str(conversation.speaker.id) != participant_id and str(conversation.listener.id) != participant_id):
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    if conversation.audio_file and os.path.exists(conversation.audio_file.path):
        response = FileResponse(conversation.audio_file, content_type='audio/wav')
        response['Content-Disposition'] = f'attachment; filename="conversation_{conversation.id}.wav"'
        return response
    else:
        return JsonResponse({'error': 'Fichier audio non trouvé'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def delete_conversation(request, conversation_id):
    """Supprimer une conversation"""
    conversation = get_object_or_404(ConversationHistory, id=conversation_id)
    participant_id = request.session.get('participant_id')
    
    # Vérifier que l'utilisateur a accès à cette conversation
    if not participant_id or (str(conversation.speaker.id) != participant_id and str(conversation.listener.id) != participant_id):
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    try:
        conversation.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class UserConversationHistoryView(ListView):
    model = ConversationHistory
    template_name = 'conference/user_history.html'
    context_object_name = 'conversations'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        # On suppose que le nom du participant correspond au username
        return ConversationHistory.objects.filter(
            speaker__nom=user.username
        ) | ConversationHistory.objects.filter(
            listener__nom=user.username
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class LastTranscriptionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        # On suppose que le nom du participant correspond au username
        conv = ConversationHistory.objects.filter(
            speaker__nom=user.username
        ).order_by('-timestamp').first()
        if not conv:
            conv = ConversationHistory.objects.filter(
                listener__nom=user.username
            ).order_by('-timestamp').first()
        if conv:
            return JsonResponse({
                'original_text': conv.original_text,
                'translated_text': conv.translated_text,
                'original_language': conv.original_language,
                'target_language': conv.target_language,
                'timestamp': conv.timestamp,
            })
        return JsonResponse({'original_text': '', 'translated_text': ''})
