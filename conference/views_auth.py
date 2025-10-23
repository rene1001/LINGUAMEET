"""
Vues d'authentification pour LinguaMeet
Style Google Meet
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .models import Room, Participant
from django.conf import settings
import uuid


class CustomUserCreationForm(UserCreationForm):
    """Formulaire personnalisé d'inscription"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Prénom'
    }))
    last_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })


class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire personnalisé de connexion"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom d\'utilisateur ou Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))


def register_view(request):
    """Vue d'inscription"""
    if request.user.is_authenticated:
        # Si une room est en attente, rediriger vers celle-ci
        next_room = request.session.get('next_room')
        if next_room:
            del request.session['next_room']
            try:
                # Valider que next_room est un UUID valide
                uuid.UUID(next_room)
                return redirect('conference:join_meeting', room_id=next_room)
            except (ValueError, AttributeError):
                pass
        return redirect('conference:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}!')
            login(request, user)
            
            # Si une room est en attente, rediriger vers celle-ci
            next_room = request.session.get('next_room')
            if next_room:
                del request.session['next_room']
                try:
                    # Valider que next_room est un UUID valide
                    uuid.UUID(next_room)
                    return redirect('conference:join_meeting', room_id=next_room)
                except (ValueError, AttributeError):
                    pass
            
            return redirect('conference:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'conference/register.html', {'form': form})


def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        # Si une room est en attente, rediriger vers celle-ci
        next_room = request.session.get('next_room')
        if next_room:
            del request.session['next_room']
            try:
                # Valider que next_room est un UUID valide
                uuid.UUID(next_room)
                return redirect('conference:join_meeting', room_id=next_room)
            except (ValueError, AttributeError):
                pass
        return redirect('conference:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username}!')
                
                # Si une room est en attente, rediriger vers celle-ci
                next_room = request.session.get('next_room')
                if next_room:
                    del request.session['next_room']
                    try:
                        # Valider que next_room est un UUID valide
                        uuid.UUID(next_room)
                        return redirect('conference:join_meeting', room_id=next_room)
                    except (ValueError, AttributeError):
                        pass
                
                return redirect('conference:home')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'conference/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('conference:login')


@login_required
def home_view(request):
    """Vue de la page d'accueil (style Google Meet)"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            # Créer une nouvelle réunion instantanément
            nom_salle = request.POST.get('nom_salle', 'Réunion rapide')
            langue_defaut = request.POST.get('langue_defaut', 'fr')
            
            room = Room.objects.create(
                nom=nom_salle,
                langue_par_defaut=langue_defaut
            )
            
            # Rediriger vers la page de partage
            return redirect('conference:room_ready', room_id=room.id)
            
        elif action == 'join':
            room_id = request.POST.get('room_id')
            try:
                # Valider l'UUID
                room = Room.objects.get(id=room_id, actif=True)
                return redirect('conference:join_meeting', room_id=room.id)
            except (Room.DoesNotExist, ValueError):
                messages.error(request, "Code de réunion invalide.")
    
    return render(request, 'conference/home_meet.html', {
        'user': request.user
    })


@login_required
def room_ready_view(request, room_id):
    """Page de réunion créée avec lien de partage (style Google Meet)"""
    room = get_object_or_404(Room, id=room_id, actif=True)
    
    # Générer l'URL complète
    meeting_url = request.build_absolute_uri(f'/join/{room.id}/')
    
    return render(request, 'conference/room_ready.html', {
        'room': room,
        'meeting_url': meeting_url,
        'room_code': str(room.id),
        'user': request.user
    })


def join_meeting_view(request, room_id):
    """Vue pour rejoindre une réunion (avec ou sans compte)"""
    room = get_object_or_404(Room, id=room_id, actif=True)
    
    # Si l'utilisateur n'est pas connecté, sauvegarder l'URL de destination
    if not request.user.is_authenticated:
        request.session['next_room'] = str(room_id)
        messages.info(request, "Connectez-vous ou créez un compte pour rejoindre la réunion.")
        return redirect('conference:login')
    
    # Rediriger vers la salle avec modale de sélection de langue
    return redirect('conference:room', room_id=room.id)


@login_required
def select_language_and_join(request, room_id):
    """API pour sélectionner la langue et rejoindre la réunion"""
    room = get_object_or_404(Room, id=room_id, actif=True)
    
    if request.method == 'POST':
        langue = request.POST.get('langue', 'fr')
        
        # Créer ou mettre à jour le participant
        participant, created = Participant.objects.get_or_create(
            room=room,
            nom=request.user.username,
            defaults={
                'langue': langue,
                'session_id': request.session.session_key or str(uuid.uuid4())
            }
        )
        
        if not created:
            # Mettre à jour la langue si le participant existe déjà
            participant.langue = langue
            participant.actif = True
            participant.save()
        
        # Stocker l'ID du participant en session
        request.session['participant_id'] = str(participant.id)
        request.session['room_id'] = str(room.id)
        
        return redirect('conference:room', room_id=room.id)
    
    return render(request, 'conference/select_language.html', {
        'room': room,
        'supported_languages': settings.SUPPORTED_LANGUAGES
    })
