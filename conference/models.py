import uuid
from django.db import models
from django.conf import settings
import os


class Room(models.Model):
    """Modèle pour représenter une salle de conférence"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom de la salle")
    langue_par_defaut = models.CharField(
        max_length=10, 
        default='fr',
        verbose_name="Langue par défaut"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Salle de conférence"
        verbose_name_plural = "Salles de conférence"

    def __str__(self):
        return f"{self.nom} ({self.id})"

    @property
    def participants_count(self):
        return self.participants.filter(actif=True).count()

    @property
    def langue_par_defaut_display(self):
        """Retourne le nom complet de la langue par défaut"""
        return settings.SUPPORTED_LANGUAGES.get(self.langue_par_defaut, self.langue_par_defaut)


class Participant(models.Model):
    """Modèle pour représenter un participant dans une salle"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom du participant")
    langue_souhaitée = models.CharField(
        max_length=10, 
        default='en',
        verbose_name="Langue de réception souhaitée"
    )
    langue_parole = models.CharField(
        max_length=10, 
        default='fr',
        verbose_name="Langue de parole"
    )
    socket_id = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name='participants',
        verbose_name="Salle"
    )
    date_join = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    micro_actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return f"{self.nom} dans {self.room.nom}"

    @property
    def langue_souhaitée_display(self):
        """Retourne le nom complet de la langue souhaitée"""
        from django.conf import settings
        return settings.SUPPORTED_LANGUAGES.get(self.langue_souhaitée, self.langue_souhaitée)

    @property
    def langue_parole_display(self):
        """Retourne le nom complet de la langue de parole"""
        from django.conf import settings
        return settings.SUPPORTED_LANGUAGES.get(self.langue_parole, self.langue_parole)


class ConversationHistory(models.Model):
    """Modèle pour l'historique des conversations audio"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations sur la conversation
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='conversations')
    speaker = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='speeches')
    listener = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='listened_conversations')
    
    # Contenu de la conversation
    original_text = models.TextField(verbose_name="Texte original")
    translated_text = models.TextField(verbose_name="Texte traduit")
    original_language = models.CharField(max_length=10, verbose_name="Langue originale")
    target_language = models.CharField(max_length=10, verbose_name="Langue cible")
    
    # Fichier audio
    audio_file = models.FileField(
        upload_to='conversations/%Y/%m/%d/',
        verbose_name="Fichier audio"
    )
    audio_duration = models.FloatField(default=0.0, verbose_name="Durée audio (secondes)")
    
    # Métadonnées
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Horodatage")
    is_archived = models.BooleanField(default=False, verbose_name="Archivé")
    
    class Meta:
        verbose_name = "Historique de conversation"
        verbose_name_plural = "Historiques de conversations"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.speaker.nom} → {self.listener.nom} ({self.timestamp.strftime('%H:%M:%S')})"

    @property
    def original_language_display(self):
        """Retourne le nom complet de la langue originale"""
        from django.conf import settings
        return settings.SUPPORTED_LANGUAGES.get(self.original_language, self.original_language)

    @property
    def target_language_display(self):
        """Retourne le nom complet de la langue cible"""
        from django.conf import settings
        return settings.SUPPORTED_LANGUAGES.get(self.target_language, self.target_language)

    @property
    def formatted_duration(self):
        """Retourne la durée formatée"""
        minutes = int(self.audio_duration // 60)
        seconds = int(self.audio_duration % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def delete(self, *args, **kwargs):
        """Supprimer le fichier audio lors de la suppression"""
        if self.audio_file:
            if os.path.isfile(self.audio_file.path):
                os.remove(self.audio_file.path)
        super().delete(*args, **kwargs)
