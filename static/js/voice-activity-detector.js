// LinguaMeet - Détecteur d'activité vocale et indicateur visuel de micro

class VoiceActivityDetector {
    constructor(stream) {
        this.stream = stream;
        this.audioContext = null;
        this.analyser = null;
        this.microphone = null;
        this.javascriptNode = null;
        this.isActive = false;
        this.threshold = 30; // Seuil de détection (0-100)
        this.smoothingTimeConstant = 0.8;
        this.fftSize = 512;
        this.volumeCallback = null;
        this.isSpeaking = false;
        this.speakingTimeout = null;
    }

    initialize() {
        try {
            // Créer le contexte audio
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.microphone = this.audioContext.createMediaStreamSource(this.stream);
            this.javascriptNode = this.audioContext.createScriptProcessor(2048, 1, 1);

            // Configurer l'analyseur
            this.analyser.smoothingTimeConstant = this.smoothingTimeConstant;
            this.analyser.fftSize = this.fftSize;

            // Connecter les nœuds
            this.microphone.connect(this.analyser);
            this.analyser.connect(this.javascriptNode);
            this.javascriptNode.connect(this.audioContext.destination);

            // Traiter l'audio
            this.javascriptNode.onaudioprocess = () => {
                if (this.isActive) {
                    this.processAudio();
                }
            };

            this.isActive = true;
            console.log('✓ Détecteur d\'activité vocale initialisé');
            return true;
        } catch (error) {
            console.error('Erreur initialisation détecteur vocal:', error);
            return false;
        }
    }

    processAudio() {
        const array = new Uint8Array(this.analyser.frequencyBinCount);
        this.analyser.getByteFrequencyData(array);
        
        // Calculer le volume moyen
        let values = 0;
        const length = array.length;
        for (let i = 0; i < length; i++) {
            values += array[i];
        }
        const average = values / length;
        
        // Normaliser à 0-100
        const volume = Math.min(100, Math.round(average));
        
        // Détecter si la personne parle
        const wasSpeaking = this.isSpeaking;
        this.isSpeaking = volume > this.threshold;
        
        // Appeler le callback avec le volume
        if (this.volumeCallback) {
            this.volumeCallback(volume, this.isSpeaking);
        }
        
        // Gérer les changements d'état
        if (this.isSpeaking && !wasSpeaking) {
            this.onSpeakingStart();
        } else if (!this.isSpeaking && wasSpeaking) {
            // Ajouter un petit délai avant de marquer comme non-parlant
            clearTimeout(this.speakingTimeout);
            this.speakingTimeout = setTimeout(() => {
                this.onSpeakingStop();
            }, 500);
        }
    }

    onSpeakingStart() {
        // Événement déclenché quand la personne commence à parler
        const event = new CustomEvent('voiceActivityStart', {
            detail: { detector: this }
        });
        window.dispatchEvent(event);
    }

    onSpeakingStop() {
        // Événement déclenché quand la personne arrête de parler
        const event = new CustomEvent('voiceActivityStop', {
            detail: { detector: this }
        });
        window.dispatchEvent(event);
    }

    setVolumeCallback(callback) {
        this.volumeCallback = callback;
    }

    setThreshold(threshold) {
        this.threshold = Math.max(0, Math.min(100, threshold));
    }

    stop() {
        this.isActive = false;
        if (this.javascriptNode) {
            this.javascriptNode.disconnect();
        }
        if (this.analyser) {
            this.analyser.disconnect();
        }
        if (this.microphone) {
            this.microphone.disconnect();
        }
        if (this.audioContext && this.audioContext.state !== 'closed') {
            this.audioContext.close();
        }
        clearTimeout(this.speakingTimeout);
        console.log('✓ Détecteur d\'activité vocale arrêté');
    }
}

// Classe pour l'indicateur visuel de micro
class MicrophoneIndicator {
    constructor(elementId, participantId) {
        this.elementId = elementId;
        this.participantId = participantId;
        this.indicator = null;
        this.waveContainer = null;
        this.volumeBars = [];
        this.isActive = false;
    }

    create() {
        // Créer l'indicateur si il n'existe pas
        let container = document.getElementById(this.elementId);
        if (!container) {
            // Chercher le conteneur du participant
            const participantElement = document.getElementById(`video-${this.participantId}`) ||
                                      document.getElementById(`participant-${this.participantId}`);
            if (!participantElement) return;
            
            container = document.createElement('div');
            container.id = this.elementId;
            container.className = 'microphone-indicator';
            participantElement.parentElement.appendChild(container);
        }

        this.indicator = container;
        
        // Créer l'interface visuelle
        this.indicator.innerHTML = `
            <div class="mic-icon-container">
                <i class="fas fa-microphone"></i>
            </div>
            <div class="voice-wave-container">
                <div class="voice-wave-bar"></div>
                <div class="voice-wave-bar"></div>
                <div class="voice-wave-bar"></div>
                <div class="voice-wave-bar"></div>
                <div class="voice-wave-bar"></div>
            </div>
        `;

        // Appliquer les styles
        this.applyStyles();
        
        this.waveContainer = this.indicator.querySelector('.voice-wave-container');
        this.volumeBars = this.indicator.querySelectorAll('.voice-wave-bar');
    }

    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .microphone-indicator {
                position: absolute;
                bottom: 50px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 16px;
                background: rgba(30, 142, 62, 0.95);
                border-radius: 24px;
                z-index: 20;
                opacity: 0;
                transition: opacity 0.3s ease;
                backdrop-filter: blur(8px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }

            .microphone-indicator.active {
                opacity: 1;
            }

            .microphone-indicator.inactive {
                background: rgba(95, 99, 104, 0.95);
            }

            .mic-icon-container {
                color: white;
                font-size: 16px;
                display: flex;
                align-items: center;
            }

            .voice-wave-container {
                display: flex;
                align-items: center;
                gap: 3px;
                height: 20px;
            }

            .voice-wave-bar {
                width: 3px;
                height: 4px;
                background: white;
                border-radius: 2px;
                transition: height 0.1s ease;
            }

            .microphone-indicator.speaking .voice-wave-bar:nth-child(1) {
                animation: voiceWave 0.6s ease-in-out infinite;
                animation-delay: 0s;
            }

            .microphone-indicator.speaking .voice-wave-bar:nth-child(2) {
                animation: voiceWave 0.6s ease-in-out infinite;
                animation-delay: 0.1s;
            }

            .microphone-indicator.speaking .voice-wave-bar:nth-child(3) {
                animation: voiceWave 0.6s ease-in-out infinite;
                animation-delay: 0.2s;
            }

            .microphone-indicator.speaking .voice-wave-bar:nth-child(4) {
                animation: voiceWave 0.6s ease-in-out infinite;
                animation-delay: 0.1s;
            }

            .microphone-indicator.speaking .voice-wave-bar:nth-child(5) {
                animation: voiceWave 0.6s ease-in-out infinite;
                animation-delay: 0s;
            }

            @keyframes voiceWave {
                0%, 100% {
                    height: 4px;
                }
                50% {
                    height: 20px;
                }
            }
        `;
        
        if (!document.getElementById('mic-indicator-styles')) {
            style.id = 'mic-indicator-styles';
            document.head.appendChild(style);
        }
    }

    show() {
        if (this.indicator) {
            this.indicator.classList.add('active');
            this.isActive = true;
        }
    }

    hide() {
        if (this.indicator) {
            this.indicator.classList.remove('active');
            this.isActive = false;
        }
    }

    updateVolume(volume, isSpeaking) {
        if (!this.indicator) return;

        if (isSpeaking) {
            this.indicator.classList.add('speaking');
            this.indicator.classList.remove('inactive');
            this.show();
        } else {
            this.indicator.classList.remove('speaking');
            // Ne pas masquer complètement, juste arrêter l'animation
        }

        // Mettre à jour la hauteur des barres en fonction du volume
        if (this.volumeBars.length > 0) {
            const normalizedVolume = volume / 100;
            this.volumeBars.forEach((bar, index) => {
                const height = 4 + (normalizedVolume * 16);
                if (!isSpeaking) {
                    bar.style.height = '4px';
                } else {
                    bar.style.height = `${height}px`;
                }
            });
        }
    }

    setMuted(muted) {
        if (!this.indicator) return;

        if (muted) {
            this.indicator.classList.add('inactive');
            this.indicator.querySelector('.mic-icon-container i').className = 'fas fa-microphone-slash';
        } else {
            this.indicator.classList.remove('inactive');
            this.indicator.querySelector('.mic-icon-container i').className = 'fas fa-microphone';
        }
    }

    destroy() {
        if (this.indicator) {
            this.indicator.remove();
        }
    }
}

// Export pour utilisation globale
if (typeof window !== 'undefined') {
    window.VoiceActivityDetector = VoiceActivityDetector;
    window.MicrophoneIndicator = MicrophoneIndicator;
}
