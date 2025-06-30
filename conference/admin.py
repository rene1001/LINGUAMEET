from django.contrib import admin
from .models import Room, Participant, ConversationHistory

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['nom', 'langue_par_defaut_display', 'participants_count', 'date_creation', 'actif']
    list_filter = ['actif', 'langue_par_defaut', 'date_creation']
    search_fields = ['nom']
    readonly_fields = ['id', 'date_creation']
    ordering = ['-date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'langue_par_defaut', 'actif')
        }),
        ('Métadonnées', {
            'fields': ('id', 'date_creation'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'room', 'langue_parole_display', 'langue_souhaitée_display', 'actif', 'micro_actif', 'date_join']
    list_filter = ['actif', 'micro_actif', 'langue_parole', 'langue_souhaitée', 'date_join', 'room']
    search_fields = ['nom', 'room__nom']
    readonly_fields = ['id', 'date_join']
    ordering = ['-date_join']
    
    fieldsets = (
        ('Informations du participant', {
            'fields': ('nom', 'room', 'langue_parole', 'langue_souhaitée')
        }),
        ('État', {
            'fields': ('actif', 'micro_actif')
        }),
        ('Connexion', {
            'fields': ('socket_id', 'session_id'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('id', 'date_join'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ConversationHistory)
class ConversationHistoryAdmin(admin.ModelAdmin):
    list_display = ['speaker', 'listener', 'original_language_display', 'target_language_display', 'audio_duration', 'timestamp', 'is_archived']
    list_filter = ['original_language', 'target_language', 'is_archived', 'timestamp', 'room']
    search_fields = ['original_text', 'translated_text', 'speaker__nom', 'listener__nom', 'room__nom']
    readonly_fields = ['id', 'timestamp', 'audio_duration']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Conversation', {
            'fields': ('room', 'speaker', 'listener')
        }),
        ('Contenu', {
            'fields': ('original_text', 'translated_text', 'original_language', 'target_language')
        }),
        ('Audio', {
            'fields': ('audio_file', 'audio_duration')
        }),
        ('Métadonnées', {
            'fields': ('is_archived', 'id', 'timestamp'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiser les requêtes avec select_related"""
        return super().get_queryset(request).select_related('speaker', 'listener', 'room') 