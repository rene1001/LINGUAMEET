// LinguaMeet - Améliorations de l'interface de conférence

class ConferenceEnhancements {
    constructor() {
        this.videoManager = null;
        this.voiceDetector = null;
        this.micIndicator = null;
        this.initialized = false;
    }

    initialize(videoManager, participantId) {
        if (this.initialized) return;
        
        this.videoManager = videoManager;
        this.participantId = participantId;
        
        // Créer les améliorations d'interface
        this.createVideoQualitySelector();
        this.createNetworkStatusBar();
        this.setupVoiceActivityDetection();
        this.setupTranslationHistory();
        
        this.initialized = true;
        console.log('✓ Améliorations de conférence initialisées');
    }

    createVideoQualitySelector() {
        // Créer un sélecteur de qualité vidéo
        const selector = document.createElement('div');
        selector.className = 'video-quality-selector';
        selector.innerHTML = `
            <button class="quality-selector-btn" id="qualityBtn" title="Qualité vidéo">
                <i class="fas fa-sliders-h"></i>
            </button>
            <div class="quality-menu" id="qualityMenu">
                <div class="quality-menu-header">
                    <i class="fas fa-video me-2"></i>
                    Qualité vidéo
                </div>
                <div class="quality-option" data-quality="hd">
                    <i class="fas fa-check quality-check"></i>
                    <div>
                        <div class="quality-name">Haute définition</div>
                        <div class="quality-desc">1280x720, 30 fps</div>
                    </div>
                </div>
                <div class="quality-option" data-quality="sd">
                    <i class="fas fa-check quality-check"></i>
                    <div>
                        <div class="quality-name">Définition standard</div>
                        <div class="quality-desc">640x480, 24 fps</div>
                    </div>
                </div>
                <div class="quality-option" data-quality="audio-only">
                    <i class="fas fa-check quality-check"></i>
                    <div>
                        <div class="quality-name">Audio seul</div>
                        <div class="quality-desc">Désactiver la vidéo</div>
                    </div>
                </div>
            </div>
        `;

        // Ajouter les styles
        const style = document.createElement('style');
        style.textContent = `
            .video-quality-selector {
                position: relative;
                display: inline-block;
            }

            .quality-selector-btn {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                border: none;
                background: #3c4043;
                color: #e8eaed;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                transition: all 0.2s;
            }

            .quality-selector-btn:hover {
                transform: scale(1.1);
                background: #5f6368;
            }

            .quality-menu {
                position: absolute;
                bottom: 70px;
                left: 50%;
                transform: translateX(-50%);
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                padding: 8px;
                display: none;
                min-width: 280px;
                z-index: 1001;
            }

            .quality-menu.show {
                display: block;
                animation: fadeInUp 0.2s ease;
            }

            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateX(-50%) translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0);
                }
            }

            .quality-menu-header {
                padding: 12px 16px;
                font-weight: 600;
                color: #202124;
                border-bottom: 1px solid #dadce0;
                margin-bottom: 4px;
            }

            .quality-option {
                padding: 12px 16px;
                cursor: pointer;
                border-radius: 4px;
                color: #202124;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: background 0.2s;
            }

            .quality-option:hover {
                background: #f8f9fa;
            }

            .quality-option.active {
                background: #e8f0fe;
            }

            .quality-check {
                width: 20px;
                color: #667eea;
                opacity: 0;
                transition: opacity 0.2s;
            }

            .quality-option.active .quality-check {
                opacity: 1;
            }

            .quality-name {
                font-weight: 500;
                font-size: 14px;
            }

            .quality-desc {
                font-size: 12px;
                color: #5f6368;
                margin-top: 2px;
            }

            .network-status-bar {
                position: fixed;
                top: 70px;
                left: 20px;
                background: rgba(60, 64, 67, 0.95);
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                display: none;
                align-items: center;
                gap: 10px;
                z-index: 1000;
                backdrop-filter: blur(10px);
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }

            .network-status-bar.show {
                display: flex;
            }

            .network-status-icon {
                font-size: 18px;
            }

            .network-status-bar.excellent { background: rgba(30, 142, 62, 0.95); }
            .network-status-bar.good { background: rgba(30, 142, 62, 0.95); }
            .network-status-bar.fair { background: rgba(249, 171, 0, 0.95); }
            .network-status-bar.poor { background: rgba(234, 67, 53, 0.95); }

            .history-toggle-btn {
                position: fixed;
                bottom: 120px;
                right: 20px;
                width: 56px;
                height: 56px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                transition: all 0.3s;
                z-index: 999;
            }

            .history-toggle-btn:hover {
                transform: scale(1.1) rotate(5deg);
                box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
            }

            .history-badge {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #ea4335;
                color: white;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 11px;
                font-weight: 600;
                border: 2px solid white;
            }
        `;

        if (!document.getElementById('conference-enhancements-styles')) {
            style.id = 'conference-enhancements-styles';
            document.head.appendChild(style);
        }

        // Insérer dans la barre de contrôles
        const controlsBar = document.querySelector('.controls-bar');
        if (controlsBar) {
            // Insérer avant le bouton "Quitter"
            const leaveBtn = controlsBar.querySelector('.leave-btn');
            if (leaveBtn) {
                controlsBar.insertBefore(selector, leaveBtn);
            } else {
                controlsBar.appendChild(selector);
            }
        }

        // Gérer les clics
        const qualityBtn = document.getElementById('qualityBtn');
        const qualityMenu = document.getElementById('qualityMenu');
        
        qualityBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            qualityMenu.classList.toggle('show');
        });

        // Fermer le menu si on clique ailleurs
        document.addEventListener('click', () => {
            qualityMenu.classList.remove('show');
        });

        // Gérer la sélection de qualité
        const options = qualityMenu.querySelectorAll('.quality-option');
        options.forEach(option => {
            option.addEventListener('click', async (e) => {
                e.stopPropagation();
                const quality = option.dataset.quality;
                
                // Mettre à jour l'état visuel
                options.forEach(opt => opt.classList.remove('active'));
                option.classList.add('active');
                
                // Changer la qualité
                if (this.videoManager) {
                    await this.videoManager.changeVideoQuality(quality);
                }
                
                qualityMenu.classList.remove('show');
            });
        });

        // Marquer la qualité actuelle
        options[0].classList.add('active'); // HD par défaut
    }

    createNetworkStatusBar() {
        const statusBar = document.createElement('div');
        statusBar.id = 'networkStatusBar';
        statusBar.className = 'network-status-bar';
        statusBar.innerHTML = `
            <i class="fas fa-wifi network-status-icon"></i>
            <div>
                <div id="networkStatusText">Qualité de connexion</div>
            </div>
        `;

        document.body.appendChild(statusBar);
    }

    updateNetworkStatus(quality, details = {}) {
        const statusBar = document.getElementById('networkStatusBar');
        const statusText = document.getElementById('networkStatusText');
        
        if (!statusBar || !statusText) return;

        const statusConfig = {
            'excellent': { 
                text: 'Connexion excellente', 
                icon: 'fa-wifi',
                show: false // Ne pas afficher si tout va bien
            },
            'good': { 
                text: 'Bonne connexion', 
                icon: 'fa-wifi',
                show: false
            },
            'fair': { 
                text: 'Connexion moyenne', 
                icon: 'fa-exclamation-triangle',
                show: true
            },
            'poor': { 
                text: 'Connexion faible', 
                icon: 'fa-exclamation-circle',
                show: true
            }
        };

        const config = statusConfig[quality] || statusConfig['good'];
        
        // Mettre à jour l'apparence
        statusBar.className = `network-status-bar ${quality}`;
        statusBar.querySelector('.network-status-icon').className = `fas ${config.icon} network-status-icon`;
        statusText.textContent = config.text;

        // Afficher/masquer selon la qualité
        if (config.show) {
            statusBar.classList.add('show');
            // Auto-masquer après 10 secondes
            setTimeout(() => {
                if (quality !== 'poor') {
                    statusBar.classList.remove('show');
                }
            }, 10000);
        } else {
            statusBar.classList.remove('show');
        }
    }

    setupVoiceActivityDetection() {
        // Obtenir le flux audio local
        if (!this.videoManager || !this.videoManager.localStream) {
            console.warn('Flux audio non disponible pour la détection vocale');
            return;
        }

        // Créer le détecteur de voix
        this.voiceDetector = new VoiceActivityDetector(this.videoManager.localStream);
        const initialized = this.voiceDetector.initialize();

        if (!initialized) {
            console.warn('Impossible d\'initialiser le détecteur vocal');
            return;
        }

        // Créer l'indicateur visuel
        this.micIndicator = new MicrophoneIndicator(
            `mic-indicator-${this.participantId}`,
            this.participantId
        );
        this.micIndicator.create();

        // Connecter le détecteur à l'indicateur
        this.voiceDetector.setVolumeCallback((volume, isSpeaking) => {
            this.micIndicator.updateVolume(volume, isSpeaking);
        });

        // Écouter les événements de début/fin de parole
        window.addEventListener('voiceActivityStart', () => {
            console.log('🎤 Détection de voix démarrée');
        });

        window.addEventListener('voiceActivityStop', () => {
            console.log('🎤 Détection de voix arrêtée');
        });

        console.log('✓ Détection d\'activité vocale activée');
    }

    setupTranslationHistory() {
        // Créer le bouton d'ouverture de l'historique
        const historyBtn = document.createElement('button');
        historyBtn.className = 'history-toggle-btn';
        historyBtn.title = 'Historique des traductions';
        historyBtn.innerHTML = `
            <i class="fas fa-history"></i>
            <span class="history-badge" id="historyBadge" style="display: none;">0</span>
        `;

        historyBtn.addEventListener('click', () => {
            if (window.translationHistory) {
                window.translationHistory.togglePanel();
            }
        });

        document.body.appendChild(historyBtn);

        // Initialiser l'historique
        if (window.translationHistory) {
            const roomId = window.ROOM_ID || 'unknown';
            const participantId = window.PARTICIPANT_ID || 'unknown';
            window.translationHistory.initialize(roomId, participantId);
        }
    }

    updateHistoryBadge(count) {
        const badge = document.getElementById('historyBadge');
        if (badge) {
            if (count > 0) {
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    onMicrophoneToggle(isActive) {
        if (this.micIndicator) {
            this.micIndicator.setMuted(!isActive);
        }
    }

    cleanup() {
        if (this.voiceDetector) {
            this.voiceDetector.stop();
        }
        if (this.micIndicator) {
            this.micIndicator.destroy();
        }
        console.log('✓ Améliorations nettoyées');
    }
}

// Créer une instance globale
const conferenceEnhancements = new ConferenceEnhancements();

// Export pour utilisation globale
if (typeof window !== 'undefined') {
    window.ConferenceEnhancements = ConferenceEnhancements;
    window.conferenceEnhancements = conferenceEnhancements;
}
