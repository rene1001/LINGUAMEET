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