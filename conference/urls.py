from django.urls import path
from . import views
from .views import UserConversationHistoryView, LastTranscriptionView

app_name = 'conference'

urlpatterns = [
    path('', views.home, name='home'),
    path('join/<uuid:room_id>/', views.join_room, name='join_room'),
    path('room/<uuid:room_id>/', views.room, name='room'),
    path('room/<uuid:room_id>/update/', views.update_participant, name='update_participant'),
    path('room/<uuid:room_id>/leave/', views.leave_room, name='leave_room'),
    path('room/<uuid:room_id>/history/', views.conversation_history, name='conversation_history'),
    path('room/<uuid:room_id>/save-conversation/', views.save_conversation, name='save_conversation'),
    path('conversation/<uuid:conversation_id>/download/', views.download_audio, name='download_audio'),
    path('conversation/<uuid:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('mon-historique/', UserConversationHistoryView.as_view(), name='user_history'),
    path('api/last-transcription/', LastTranscriptionView.as_view(), name='api_last_transcription'),
] 