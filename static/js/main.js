// LinguaMeet - JavaScript principal

// Fonctions utilitaires
const LinguaMeet = {
    // Afficher un message système
    showSystemMessage: function(message, type = 'info') {
        const messagesContainer = document.getElementById('system-messages');
        if (!messagesContainer) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-sm fade-in`;
        alertDiv.innerHTML = `
            <small>
                <i class="fas fa-info-circle me-1"></i>
                ${message}
            </small>
        `;

        messagesContainer.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    },

    // Formater un UUID pour l'affichage
    formatUUID: function(uuid) {
        return uuid.replace(/(.{8})(.{4})(.{4})(.{4})(.{12})/, '$1-$2-$3-$4-$5');
    },

    // Copier du texte dans le presse-papiers
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showSystemMessage('Copié dans le presse-papiers !', 'success');
        }).catch(() => {
            this.showSystemMessage('Erreur lors de la copie', 'danger');
        });
    },

    // Vérifier si le navigateur supporte WebRTC
    checkWebRTCSupport: function() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    },

    // Obtenir les permissions microphone
    requestMicrophonePermission: async function() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: true,
                video: false 
            });
            return { success: true, stream };
        } catch (error) {
            console.error('Erreur permission microphone:', error);
            return { success: false, error: error.message };
        }
    },

    // Obtenir les permissions microphone et caméra
    requestMediaPermissions: async function(audio = true, video = true) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: audio,
                video: video ? {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                } : false
            });
            return { success: true, stream };
        } catch (error) {
            console.error('Erreur permissions média:', error);
            return { success: false, error: error.message };
        }
    },

    // Animer les barres audio
    animateAudioBars: function(containerId, isActive = false) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const bars = container.querySelectorAll('.audio-bar');
        
        if (isActive) {
            bars.forEach((bar, index) => {
                bar.style.animation = `audioWave 1s ease-in-out infinite`;
                bar.style.animationDelay = `${index * 0.1}s`;
            });
        } else {
            bars.forEach(bar => {
                bar.style.animation = 'none';
                bar.style.height = '10px';
                bar.style.opacity = '0.6';
            });
        }
    },

    // Mettre à jour le statut de connexion
    updateConnectionStatus: function(isConnected) {
        const statusElement = document.querySelector('.alert-success');
        if (!statusElement) return;

        if (isConnected) {
            statusElement.className = 'alert alert-success';
            statusElement.innerHTML = `
                <i class="fas fa-wifi me-2"></i>
                <strong>Connecté</strong>
                <br>
                <small>WebSocket actif</small>
            `;
        } else {
            statusElement.className = 'alert alert-danger';
            statusElement.innerHTML = `
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Déconnecté</strong>
                <br>
                <small>Tentative de reconnexion...</small>
            `;
        }
    },

    // Logger avec timestamp
    log: function(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const prefix = `[${timestamp}]`;
        
        switch (type) {
            case 'error':
                console.error(`${prefix} ${message}`);
                break;
            case 'warn':
                console.warn(`${prefix} ${message}`);
                break;
            default:
                console.log(`${prefix} ${message}`);
        }
    }
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier le support WebRTC
    if (!LinguaMeet.checkWebRTCSupport()) {
        LinguaMeet.showSystemMessage(
            'Votre navigateur ne supporte pas WebRTC. Veuillez utiliser un navigateur moderne.',
            'warning'
        );
    }

    // Gestionnaire pour les boutons de copie
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            LinguaMeet.copyToClipboard(textToCopy);
        });
    });

    // Gestionnaire pour les tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    const helpBanner = document.getElementById('help-banner');
    const helpClose = document.getElementById('help-banner-close');
    if (helpBanner && helpClose) {
        const seen = localStorage.getItem('lm_help_seen');
        if (seen !== '1') {
            helpBanner.style.display = 'block';
        }
        helpClose.addEventListener('click', function() {
            helpBanner.style.display = 'none';
            localStorage.setItem('lm_help_seen', '1');
        });
    }

    const themeToggle = document.getElementById('themeToggle');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');

    function applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
        const icon = themeToggle ? themeToggle.querySelector('i') : null;
        if (icon && themeToggle) {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                themeToggle.setAttribute('aria-label', 'Basculer en thème clair');
                themeToggle.title = 'Thème clair';
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                themeToggle.setAttribute('aria-label', 'Basculer en thème sombre');
                themeToggle.title = 'Thème sombre';
            }
        }
    }

    function applyFontScale(scalePct) {
        const pct = Math.min(150, Math.max(90, scalePct));
        document.documentElement.style.setProperty('--font-scale', pct + '%');
        if (zoomInBtn) zoomInBtn.title = `Zoom texte: ${pct}%`;
        if (zoomOutBtn) zoomOutBtn.title = `Zoom texte: ${pct}%`;
    }

    const savedTheme = localStorage.getItem('lm_theme') || 'light';
    applyTheme(savedTheme);

    const savedScale = parseInt(localStorage.getItem('lm_font_scale') || '100', 10);
    applyFontScale(savedScale);

    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('lm_theme', next);
        });
    }

    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', function() {
            const current = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--font-scale'), 10) || savedScale;
            const next = Math.min(150, current + 10);
            applyFontScale(next);
            localStorage.setItem('lm_font_scale', String(next));
        });
    }

    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', function() {
            const current = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--font-scale'), 10) || savedScale;
            const next = Math.max(90, current - 10);
            applyFontScale(next);
            localStorage.setItem('lm_font_scale', String(next));
        });
    }

    LinguaMeet.log('LinguaMeet initialisé');
});

// Gestionnaire d'erreurs global
window.addEventListener('error', function(event) {
    LinguaMeet.log(`Erreur JavaScript: ${event.message}`, 'error');
});

// Gestionnaire pour les promesses non gérées
window.addEventListener('unhandledrejection', function(event) {
    LinguaMeet.log(`Promesse rejetée: ${event.reason}`, 'error');
}); 