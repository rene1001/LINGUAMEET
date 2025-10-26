// LinguaMeet - Système de logs et gestion d'erreurs client

class ErrorLogger {
    constructor() {
        this.logs = [];
        this.errors = [];
        this.maxLogs = 1000;
        this.maxErrors = 100;
        this.sessionId = this.generateSessionId();
        this.startTime = new Date();
        
        // Configuration
        this.config = {
            enableConsoleCapture: true,
            enableErrorCapture: true,
            enableNetworkCapture: true,
            enablePerformanceTracking: true,
            sendToServer: false, // À activer si endpoint disponible
            serverEndpoint: '/api/logs/'
        };
        
        // Statistiques
        this.stats = {
            errors: 0,
            warnings: 0,
            info: 0,
            debug: 0
        };
    }

    initialize() {
        // Capturer les erreurs JavaScript
        if (this.config.enableErrorCapture) {
            this.setupErrorCapture();
        }

        // Capturer les logs console
        if (this.config.enableConsoleCapture) {
            this.setupConsoleCapture();
        }

        // Capturer les erreurs réseau
        if (this.config.enableNetworkCapture) {
            this.setupNetworkCapture();
        }

        // Capturer les erreurs WebRTC
        this.setupWebRTCCapture();

        console.log('✓ Système de logs initialisé');
        this.log('info', 'Logger', 'Système de logs démarré', { sessionId: this.sessionId });
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    setupErrorCapture() {
        // Erreurs JavaScript globales
        window.addEventListener('error', (event) => {
            this.logError('JavaScript', event.message, {
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error ? event.error.stack : null
            });
        });

        // Promesses non gérées
        window.addEventListener('unhandledrejection', (event) => {
            this.logError('Promise', event.reason, {
                promise: event.promise
            });
        });
    }

    setupConsoleCapture() {
        // Sauvegarder les méthodes originales
        const originalConsole = {
            log: console.log,
            error: console.error,
            warn: console.warn,
            info: console.info,
            debug: console.debug
        };

        // Wrapper pour console.error
        console.error = (...args) => {
            originalConsole.error.apply(console, args);
            this.log('error', 'Console', args.join(' '));
        };

        // Wrapper pour console.warn
        console.warn = (...args) => {
            originalConsole.warn.apply(console, args);
            this.log('warning', 'Console', args.join(' '));
        };

        // Wrapper pour console.info
        console.info = (...args) => {
            originalConsole.info.apply(console, args);
            this.log('info', 'Console', args.join(' '));
        };

        // Garder la référence
        this.originalConsole = originalConsole;
    }

    setupNetworkCapture() {
        // Intercepter fetch
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const startTime = performance.now();
            try {
                const response = await originalFetch.apply(window, args);
                const duration = performance.now() - startTime;
                
                this.log('info', 'Network', `Fetch: ${args[0]}`, {
                    method: args[1]?.method || 'GET',
                    status: response.status,
                    duration: Math.round(duration) + 'ms'
                });
                
                return response;
            } catch (error) {
                const duration = performance.now() - startTime;
                this.logError('Network', `Fetch failed: ${args[0]}`, {
                    method: args[1]?.method || 'GET',
                    error: error.message,
                    duration: Math.round(duration) + 'ms'
                });
                throw error;
            }
        };

        // Intercepter WebSocket
        const originalWebSocket = window.WebSocket;
        window.WebSocket = function(...args) {
            const ws = new originalWebSocket(...args);
            
            ws.addEventListener('open', () => {
                errorLogger.log('info', 'WebSocket', `Connected to ${args[0]}`);
            });
            
            ws.addEventListener('error', (event) => {
                errorLogger.logError('WebSocket', `Connection error: ${args[0]}`, event);
            });
            
            ws.addEventListener('close', (event) => {
                errorLogger.log('warning', 'WebSocket', `Disconnected: ${args[0]}`, {
                    code: event.code,
                    reason: event.reason
                });
            });
            
            return ws;
        };
    }

    setupWebRTCCapture() {
        // Capturer les erreurs de getUserMedia
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const originalGetUserMedia = navigator.mediaDevices.getUserMedia;
            navigator.mediaDevices.getUserMedia = async function(constraints) {
                try {
                    errorLogger.log('info', 'WebRTC', 'getUserMedia requested', constraints);
                    const stream = await originalGetUserMedia.call(navigator.mediaDevices, constraints);
                    errorLogger.log('info', 'WebRTC', 'getUserMedia succeeded');
                    return stream;
                } catch (error) {
                    errorLogger.logError('WebRTC', 'getUserMedia failed', {
                        error: error.name,
                        message: error.message,
                        constraints: constraints
                    });
                    throw error;
                }
            };
        }
    }

    log(level, source, message, details = null) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            level: level,
            source: source,
            message: message,
            details: details,
            sessionId: this.sessionId
        };

        // Ajouter aux logs
        this.logs.push(logEntry);
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        // Mettre à jour les stats
        if (this.stats.hasOwnProperty(level)) {
            this.stats[level]++;
        }

        // Envoyer au serveur si configuré
        if (this.config.sendToServer && level === 'error') {
            this.sendLogToServer(logEntry);
        }

        return logEntry;
    }

    logError(source, message, details = null) {
        const error = this.log('error', source, message, details);
        
        this.errors.push(error);
        if (this.errors.length > this.maxErrors) {
            this.errors.shift();
        }

        // Afficher notification utilisateur pour erreurs critiques
        this.showErrorNotification(source, message);

        return error;
    }

    showErrorNotification(source, message) {
        // Créer une notification d'erreur pour l'utilisateur
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.innerHTML = `
            <div class="error-notification-content">
                <i class="fas fa-exclamation-triangle"></i>
                <div>
                    <strong>${source}</strong>
                    <p>${message}</p>
                </div>
                <button class="error-notification-close">&times;</button>
            </div>
        `;

        // Ajouter les styles si pas encore fait
        if (!document.getElementById('error-logger-styles')) {
            const style = document.createElement('style');
            style.id = 'error-logger-styles';
            style.textContent = `
                .error-notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #fff;
                    border-left: 4px solid #ea4335;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    border-radius: 8px;
                    padding: 16px;
                    max-width: 400px;
                    z-index: 10000;
                    animation: slideIn 0.3s ease;
                }

                @keyframes slideIn {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                .error-notification-content {
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                }

                .error-notification-content i {
                    color: #ea4335;
                    font-size: 24px;
                    margin-top: 4px;
                }

                .error-notification-content strong {
                    color: #202124;
                    font-size: 14px;
                    display: block;
                    margin-bottom: 4px;
                }

                .error-notification-content p {
                    color: #5f6368;
                    font-size: 13px;
                    margin: 0;
                    line-height: 1.4;
                }

                .error-notification-close {
                    background: none;
                    border: none;
                    color: #5f6368;
                    font-size: 24px;
                    cursor: pointer;
                    padding: 0;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: background 0.2s;
                }

                .error-notification-close:hover {
                    background: #f8f9fa;
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        // Bouton fermer
        notification.querySelector('.error-notification-close').addEventListener('click', () => {
            notification.remove();
        });

        // Auto-fermer après 10 secondes
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }

    async sendLogToServer(logEntry) {
        if (!this.config.serverEndpoint) return;

        try {
            await fetch(this.config.serverEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(logEntry)
            });
        } catch (error) {
            // Ne pas logger cette erreur pour éviter une boucle
            console.error('Failed to send log to server:', error);
        }
    }

    exportLogs(format = 'json') {
        const exportData = {
            sessionId: this.sessionId,
            startTime: this.startTime.toISOString(),
            endTime: new Date().toISOString(),
            stats: this.stats,
            userAgent: navigator.userAgent,
            logs: this.logs,
            errors: this.errors
        };

        let content, filename, mimeType;

        if (format === 'json') {
            content = JSON.stringify(exportData, null, 2);
            filename = `linguameet_logs_${this.sessionId}.json`;
            mimeType = 'application/json';
        } else if (format === 'txt') {
            content = this.logsToText(exportData);
            filename = `linguameet_logs_${this.sessionId}.txt`;
            mimeType = 'text/plain';
        }

        // Télécharger
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        console.log(`✓ Logs exportés: ${filename}`);
    }

    logsToText(exportData) {
        let text = '=== LINGUAMEET LOGS ===\n\n';
        text += `Session ID: ${exportData.sessionId}\n`;
        text += `Start: ${exportData.startTime}\n`;
        text += `End: ${exportData.endTime}\n`;
        text += `User Agent: ${exportData.userAgent}\n\n`;
        text += `Statistics:\n`;
        text += `  Errors: ${exportData.stats.errors}\n`;
        text += `  Warnings: ${exportData.stats.warnings}\n`;
        text += `  Info: ${exportData.stats.info}\n\n`;
        text += '='.repeat(60) + '\n\n';

        // Erreurs
        if (exportData.errors.length > 0) {
            text += 'ERRORS:\n';
            text += '='.repeat(60) + '\n';
            exportData.errors.forEach(error => {
                text += `[${error.timestamp}] ${error.source}: ${error.message}\n`;
                if (error.details) {
                    text += `  Details: ${JSON.stringify(error.details, null, 2)}\n`;
                }
                text += '\n';
            });
            text += '\n';
        }

        // Tous les logs
        text += 'ALL LOGS:\n';
        text += '='.repeat(60) + '\n';
        exportData.logs.forEach(log => {
            text += `[${log.timestamp}] [${log.level.toUpperCase()}] ${log.source}: ${log.message}\n`;
            if (log.details) {
                text += `  ${JSON.stringify(log.details)}\n`;
            }
        });

        return text;
    }

    showLogViewer() {
        // Créer un viewer de logs dans l'interface
        let viewer = document.getElementById('log-viewer');
        
        if (viewer) {
            viewer.remove();
            return;
        }

        viewer = document.createElement('div');
        viewer.id = 'log-viewer';
        viewer.innerHTML = `
            <div class="log-viewer-container">
                <div class="log-viewer-header">
                    <h3><i class="fas fa-clipboard-list me-2"></i>Logs de débogage</h3>
                    <div class="log-viewer-actions">
                        <button class="log-viewer-btn" onclick="errorLogger.exportLogs('json')">
                            <i class="fas fa-download"></i> JSON
                        </button>
                        <button class="log-viewer-btn" onclick="errorLogger.exportLogs('txt')">
                            <i class="fas fa-download"></i> TXT
                        </button>
                        <button class="log-viewer-btn" onclick="errorLogger.clearLogs()">
                            <i class="fas fa-trash"></i> Effacer
                        </button>
                        <button class="log-viewer-close" onclick="document.getElementById('log-viewer').remove()">
                            &times;
                        </button>
                    </div>
                </div>
                <div class="log-viewer-stats">
                    <span class="log-stat log-stat-error">Erreurs: ${this.stats.errors}</span>
                    <span class="log-stat log-stat-warning">Avertissements: ${this.stats.warnings}</span>
                    <span class="log-stat log-stat-info">Infos: ${this.stats.info}</span>
                </div>
                <div class="log-viewer-content" id="log-viewer-content"></div>
            </div>
        `;

        // Styles
        const style = document.createElement('style');
        style.textContent = `
            #log-viewer {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 90%;
                max-width: 1000px;
                height: 80vh;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                z-index: 10001;
                display: flex;
                flex-direction: column;
            }

            .log-viewer-container {
                display: flex;
                flex-direction: column;
                height: 100%;
            }

            .log-viewer-header {
                padding: 20px;
                border-bottom: 1px solid #dadce0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .log-viewer-header h3 {
                margin: 0;
                font-size: 18px;
                color: #202124;
            }

            .log-viewer-actions {
                display: flex;
                gap: 10px;
                align-items: center;
            }

            .log-viewer-btn {
                padding: 6px 12px;
                border: 1px solid #dadce0;
                background: white;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
                transition: all 0.2s;
            }

            .log-viewer-btn:hover {
                background: #f8f9fa;
            }

            .log-viewer-close {
                background: none;
                border: none;
                font-size: 28px;
                color: #5f6368;
                cursor: pointer;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
            }

            .log-viewer-close:hover {
                background: #f8f9fa;
            }

            .log-viewer-stats {
                padding: 12px 20px;
                background: #f8f9fa;
                display: flex;
                gap: 20px;
                border-bottom: 1px solid #dadce0;
            }

            .log-stat {
                font-size: 13px;
                font-weight: 500;
            }

            .log-stat-error { color: #ea4335; }
            .log-stat-warning { color: #f9ab00; }
            .log-stat-info { color: #1e8e3e; }

            .log-viewer-content {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background: #202124;
                color: #e8eaed;
            }

            .log-entry {
                margin-bottom: 8px;
                padding: 8px;
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.05);
            }

            .log-entry-error { border-left: 3px solid #ea4335; }
            .log-entry-warning { border-left: 3px solid #f9ab00; }
            .log-entry-info { border-left: 3px solid #1e8e3e; }

            .log-entry-time { color: #9aa0a6; }
            .log-entry-source { color: #8ab4f8; font-weight: 600; }
            .log-entry-message { color: #e8eaed; }
        `;
        document.head.appendChild(style);

        document.body.appendChild(viewer);

        // Remplir avec les logs
        this.updateLogViewer();
    }

    updateLogViewer() {
        const content = document.getElementById('log-viewer-content');
        if (!content) return;

        content.innerHTML = this.logs.map(log => `
            <div class="log-entry log-entry-${log.level}">
                <span class="log-entry-time">[${new Date(log.timestamp).toLocaleTimeString()}]</span>
                <span class="log-entry-source">[${log.source}]</span>
                <span class="log-entry-message">${log.message}</span>
                ${log.details ? `<pre style="margin: 4px 0 0 0; color: #9aa0a6;">${JSON.stringify(log.details, null, 2)}</pre>` : ''}
            </div>
        `).join('');

        // Scroll en bas
        content.scrollTop = content.scrollHeight;
    }

    clearLogs() {
        if (confirm('Effacer tous les logs ?')) {
            this.logs = [];
            this.errors = [];
            this.stats = { errors: 0, warnings: 0, info: 0, debug: 0 };
            this.updateLogViewer();
            console.log('✓ Logs effacés');
        }
    }

    getStats() {
        return {
            ...this.stats,
            totalLogs: this.logs.length,
            totalErrors: this.errors.length,
            sessionDuration: Math.round((Date.now() - this.startTime.getTime()) / 1000) + 's'
        };
    }
}

// Créer une instance globale
const errorLogger = new ErrorLogger();

// Export
if (typeof window !== 'undefined') {
    window.ErrorLogger = ErrorLogger;
    window.errorLogger = errorLogger;
    
    // Commande console pratique
    window.showLogs = () => errorLogger.showLogViewer();
}
