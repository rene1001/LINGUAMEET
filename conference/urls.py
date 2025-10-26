from django.urls import path
from . import views
from .views import UserConversationHistoryView, LastTranscriptionView, translate_test
from . import views_auth

app_name = 'conference'

urlpatterns = [
    # Authentification
    path('login/', views_auth.login_view, name='login'),
    path('register/', views_auth.register_view, name='register'),
    path('logout/', views_auth.logout_view, name='logout'),
    
    # Page d'accueil style Google Meet
    path('', views_auth.home_view, name='home'),
    path('about/', views.about, name='about'),
    
    # Flux Google Meet - Création et partage
    path('ready/<uuid:room_id>/', views_auth.room_ready_view, name='room_ready'),
    path('join/<uuid:room_id>/', views_auth.join_meeting_view, name='join_meeting'),
    path('select-language/<uuid:room_id>/', views_auth.select_language_and_join, name='select_language'),
    
    # Salle de conférence
    path('room/<uuid:room_id>/', views.room, name='room'),
    path('room/<uuid:room_id>/test/', views.device_test, name='device_test'),
    path('room/<uuid:room_id>/leave/', views.leave_room, name='leave_room'),
    path('room/<uuid:room_id>/update/', views.update_participant, name='update_participant'),
    path('room/<uuid:room_id>/history/', views.conversation_history, name='conversation_history'),
    path('room/<uuid:room_id>/save-conversation/', views.save_conversation, name='save_conversation'),
    
    # Historique
    path('conversation/<uuid:conversation_id>/download/', views.download_audio, name='download_audio'),
    path('conversation/<uuid:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('mon-historique/', UserConversationHistoryView.as_view(), name='user_history'),
    path('api/last-transcription/', LastTranscriptionView.as_view(), name='api_last_transcription'),
    path('api/translate-test/', translate_test, name='api_translate_test'),
]