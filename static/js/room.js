// LinguaMeet - JavaScript pour la salle de conférence

class ConferenceRoom {
    constructor() {
        this.roomId = ROOM_ID;
        this.participantId = PARTICIPANT_ID;
        this.participantName = PARTICIPANT_NAME;
        this.participantLanguage = PARTICIPANT_LANGUAGE;
        this.participantReceptionLanguage = PARTICIPANT_RECEPTION_LANGUAGE;
        
        this.websocket = null;
        this.mediaRecorder = null;
        this.audioStream = null;
        this.isMicrophoneActive = true;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        this.audioContext = null;
        this.audioDestination = null;
        
        this.init();
    }

    async init() {
        try {
            // Demander permission microphone
            const permissionResult = await LinguaMeet.requestMicrophonePermission();
            if (!permissionResult.success) {
                LinguaMeet.showSystemMessage(
                    `Erreur microphone: ${permissionResult.error}`,
                    'danger'
                );
                return;
            }

            this.audioStream = permissionResult.stream;
            this.setupAudioContext();
            this.setupWebSocket();
            this.setupEventListeners();
            
            LinguaMeet.log('Salle de conférence initialisée');
        } catch (error) {
            LinguaMeet.log(`Erreur initialisation: ${error.message}`, 'error');
        }
    }

    setupAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.audioDestination = this.audioContext.createMediaStreamDestination();
            
            // Connecter le stream microphone à l'audio context
            const source = this.audioContext.createMediaStreamSource(this.audioStream);
            source.connect(this.audioDestination);
            
            LinguaMeet.log('Contexte audio configuré');
        } catch (error) {
            LinguaMeet.log(`Erreur contexte audio: ${error.message}`, 'error');
        }
    }

    setupWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/conference/${this.roomId}/`;
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            this.isConnected = true;
            this.reconnectAttempts = 0;
            LinguaMeet.updateConnectionStatus(true);
            LinguaMeet.showSystemMessage('Connecté à la salle de conférence', 'success');
            
            // Envoyer les informations du participant
            this.sendMessage({
                type: 'join',
                participant_id: this.participantId,
                name: this.participantName,
                language: this.participantLanguage,
                reception_language: this.participantReceptionLanguage
            });
        };

        this.websocket.onmessage = (event) => {
            this.handleWebSocketMessage(event.data);
        };

        this.websocket.onclose = () => {
            this.isConnected = false;
            LinguaMeet.updateConnectionStatus(false);
            LinguaMeet.showSystemMessage('Déconnecté de la salle', 'warning');
            
            // Tentative de reconnexion
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.reconnectAttempts++;
                setTimeout(() => {
                    LinguaMeet.showSystemMessage(`Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts}`, 'info');
                    this.setupWebSocket();
                }, 2000 * this.reconnectAttempts);
            }
        };

        this.websocket.onerror = (error) => {
            LinguaMeet.log(`Erreur WebSocket: ${error}`, 'error');
        };
    }

    setupEventListeners() {
        // Bouton microphone
        const micButton = document.getElementById('microphone-btn');
        if (micButton) {
            micButton.addEventListener('click', () => {
                this.toggleMicrophone();
            });
        }

        // Sélecteur de langue de réception
        const languageSelect = document.getElementById('reception-language');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.updateReceptionLanguage(e.target.value);
            });
        }

        // Gestionnaire de fermeture de page
        window.addEventListener('beforeunload', () => {
            this.leaveRoom();
        });
    }

    toggleMicrophone() {
        this.isMicrophoneActive = !this.isMicrophoneActive;
        
        const micButton = document.getElementById('microphone-btn');
        const participantCard = document.getElementById(`participant-${this.participantId}`);
        
        if (this.isMicrophoneActive) {
            micButton.className = 'btn btn-lg btn-success';
            micButton.innerHTML = '<i class="fas fa-microphone me-2"></i>Microphone ACTIF';
            participantCard.className = 'card participant-card microphone-active';
            LinguaMeet.showSystemMessage('Microphone activé', 'success');
        } else {
            micButton.className = 'btn btn-lg btn-danger';
            micButton.innerHTML = '<i class="fas fa-microphone-slash me-2"></i>Microphone INACTIF';
            participantCard.className = 'card participant-card microphone-inactive';
            LinguaMeet.showSystemMessage('Microphone désactivé', 'warning');
        }

        // Envoyer l'état au serveur
        this.sendMessage({
            type: 'microphone_toggle',
            active: this.isMicrophoneActive
        });
    }

    updateReceptionLanguage(language) {
        this.participantReceptionLanguage = language;
        
        // Envoyer la mise à jour au serveur
        fetch(`/room/${this.roomId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify({
                langue_souhaitée: language
            })
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                LinguaMeet.showSystemMessage(`Langue de réception mise à jour`, 'success');
            }
        }).catch(error => {
            LinguaMeet.log(`Erreur mise à jour langue: ${error}`, 'error');
        });
    }

    sendMessage(message) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(message));
        }
    }

    handleWebSocketMessage(data) {
        try {
            const message = JSON.parse(data);
            
            switch (message.type) {
                case 'participant_joined':
                    this.handleParticipantJoined(message);
                    break;
                case 'participant_left':
                    this.handleParticipantLeft(message);
                    break;
                case 'audio_translated':
                    this.handleTranslatedAudio(message);
                    break;
                case 'system_message':
                    LinguaMeet.showSystemMessage(message.content, message.message_type || 'info');
                    break;
                case 'participant_update':
                    this.handleParticipantUpdate(message);
                    break;
                case 'transcription':
                    this.handleTranscription(message);
                    break;
                case 'last_transcription':
                    this.handleLastTranscription(message);
                    break;
                default:
                    LinguaMeet.log(`Message non reconnu: ${message.type}`, 'warn');
            }
        } catch (error) {
            LinguaMeet.log(`Erreur parsing message: ${error}`, 'error');
        }
    }

    handleParticipantJoined(message) {
        const { participant_id, name, language, reception_language } = message;
        
        // Créer la carte du participant
        const participantHtml = `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card participant-card fade-in" id="participant-${participant_id}">
                    <div class="card-body text-center">
                        <div class="mb-2">
                            <i class="fas fa-user-circle text-secondary" style="font-size: 2.5rem;"></i>
                        </div>
                        <h6 class="card-title mb-1">${name}</h6>
                        <div class="mb-2">
                            <span class="badge bg-primary me-1">
                                <i class="fas fa-microphone me-1"></i>${this.getLanguageName(language)}
                            </span>
                            <span class="badge bg-success">
                                <i class="fas fa-headphones me-1"></i>${this.getLanguageName(reception_language)}
                            </span>
                        </div>
                        <div class="audio-visualizer" id="audio-viz-${participant_id}">
                            <div class="audio-bar"></div>
                            <div class="audio-bar"></div>
                            <div class="audio-bar"></div>
                            <div class="audio-bar"></div>
                            <div class="audio-bar"></div>
                        </div>
                        <small class="text-muted">
                            <i class="fas fa-circle text-success me-1"></i>En ligne
                        </small>
                    </div>
                </div>
            </div>
        `;
        
        const container = document.getElementById('participants-container');
        container.insertAdjacentHTML('beforeend', participantHtml);
        
        LinguaMeet.showSystemMessage(`${name} a rejoint la réunion`, 'success');
    }

    handleParticipantLeft(message) {
        const { participant_id, name } = message;
        
        const participantElement = document.getElementById(`participant-${participant_id}`);
        if (participantElement) {
            participantElement.remove();
        }
        
        LinguaMeet.showSystemMessage(`${name} a quitté la réunion`, 'warning');
    }

    async handleTranslatedAudio(message) {
        const { audio_data, participant_name, original_text, translated_text } = message;
        
        try {
            // Convertir l'audio base64 en ArrayBuffer
            const audioArrayBuffer = this.base64ToArrayBuffer(audio_data);
            
            // Décoder l'audio
            const audioBuffer = await this.audioContext.decodeAudioData(audioArrayBuffer);
            
            // Créer une source audio et la connecter
            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioContext.destination);
            
            // Jouer l'audio
            source.start(0);
            
            // Animer les barres audio du participant
            LinguaMeet.animateAudioBars(`audio-viz-${message.participant_id}`, true);
            setTimeout(() => {
                LinguaMeet.animateAudioBars(`audio-viz-${message.participant_id}`, false);
            }, 3000);
            
            // Afficher le message de traduction
            LinguaMeet.showSystemMessage(
                `${participant_name}: "${original_text}" → "${translated_text}"`,
                'info'
            );
            
            updateLiveTranscription({
                who: 'me',
                original_text: original_text,
                translated_text: translated_text
            });
        } catch (error) {
            LinguaMeet.log(`Erreur lecture audio: ${error}`, 'error');
        }
    }

    handleParticipantUpdate(message) {
        const { participant_id, updates } = message;
        
        const participantElement = document.getElementById(`participant-${participant_id}`);
        if (!participantElement) return;
        
        if (updates.microphone_active !== undefined) {
            const card = participantElement.querySelector('.card');
            if (updates.microphone_active) {
                card.className = 'card participant-card microphone-active';
            } else {
                card.className = 'card participant-card microphone-inactive';
            }
        }
        
        if (updates.reception_language) {
            const badge = participantElement.querySelector('.badge.bg-success');
            if (badge) {
                badge.innerHTML = `<i class="fas fa-headphones me-1"></i>${this.getLanguageName(updates.reception_language)}`;
            }
        }
    }

    handleTranscription(message) {
        const { text } = message;
        updateLiveTranscription({
            who: 'received',
            original_text: text,
            translated_text: text
        });
    }

    handleLastTranscription(message) {
        const { text } = message;
        updateLiveTranscription({
            who: 'received',
            original_text: text,
            translated_text: text
        });
    }

    getLanguageName(code) {
        const languages = {
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ja': '日本語',
            'ko': '한국어',
            'zh': '中文'
        };
        return languages[code] || code;
    }

    base64ToArrayBuffer(base64) {
        const binaryString = window.atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
    }

    leaveRoom() {
        if (this.websocket) {
            this.websocket.close();
        }
        
        if (this.audioStream) {
            this.audioStream.getTracks().forEach(track => track.stop());
        }
        
        if (this.audioContext) {
            this.audioContext.close();
        }
    }
}

// Initialiser la salle de conférence
let conferenceRoom;
document.addEventListener('DOMContentLoaded', function() {
    conferenceRoom = new ConferenceRoom();
});

// Fonctions utilitaires globales pour la transcription en direct
if (!document.getElementById('live-transcription-container')) {
    const liveDiv = document.createElement('div');
    liveDiv.id = 'live-transcription-container';
    liveDiv.style.position = 'fixed';
    liveDiv.style.bottom = '0';
    liveDiv.style.left = '0';
    liveDiv.style.width = '100%';
    liveDiv.style.background = '#f8f9fa';
    liveDiv.style.borderTop = '1px solid #ddd';
    liveDiv.style.padding = '10px 20px';
    liveDiv.style.zIndex = '1000';
    liveDiv.innerHTML = '<span id="live-transcription-label">Transcription en temps réel :</span> <span id="live-transcription-text" style="font-weight:bold"></span>';
    document.body.appendChild(liveDiv);
}

function updateLiveTranscription(data) {
    const label = document.getElementById('live-transcription-label');
    const text = document.getElementById('live-transcription-text');
    if (data.who === 'me') {
        label.textContent = 'Vous (transcription envoyée) :';
        text.textContent = data.original_text + '  |  ' + data.translated_text;
    } else {
        label.textContent = 'Reçu (transcription reçue) :';
        text.textContent = data.original_text + '  |  ' + data.translated_text;
    }
}

// Quand l'utilisateur parle (microphone activé), afficher la transcription en direct
function onUserSpeechTranscribed(text) {
    updateLiveTranscription({
        who: 'me',
        original_text: text,
        translated_text: text
    });
} 