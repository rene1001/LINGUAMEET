// LinguaMeet - Optimiseur de performance

class PerformanceOptimizer {
    constructor(videoManager) {
        this.videoManager = videoManager;
        this.isMonitoring = false;
        this.monitoringInterval = null;
        
        // Métriques de performance
        this.cpuUsage = 0;
        this.memoryUsage = 0;
        this.frameRate = 30;
        this.droppedFrames = 0;
        
        // Seuils de performance
        this.thresholds = {
            cpuHigh: 70,        // Pourcentage CPU considéré élevé
            cpuCritical: 85,    // CPU critique
            memoryHigh: 70,     // Pourcentage mémoire élevé
            frameRateLow: 15,   // FPS minimal acceptable
            inactivityTime: 10000 // 10 secondes d'inactivité
        };
        
        // État d'optimisation
        this.optimizationMode = 'normal'; // 'normal', 'economy', 'ultra-economy'
        this.lastActivityTime = Date.now();
        this.isUserActive = true;
        
        // Compression adaptative
        this.compressionSettings = {
            normal: { maxBitrate: 2500000, scaleResolutionDownBy: 1 },
            economy: { maxBitrate: 1000000, scaleResolutionDownBy: 2 },
            'ultra-economy': { maxBitrate: 500000, scaleResolutionDownBy: 4 }
        };
    }

    startMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        
        // Surveiller toutes les 3 secondes
        this.monitoringInterval = setInterval(() => {
            this.checkPerformance();
            this.optimizeIfNeeded();
        }, 3000);
        
        // Détecter l'activité utilisateur
        this.setupActivityDetection();
        
        console.log('✓ Surveillance de performance démarrée');
    }

    stopMonitoring() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
        }
        this.isMonitoring = false;
        console.log('✓ Surveillance de performance arrêtée');
    }

    async checkPerformance() {
        try {
            // Vérifier l'utilisation mémoire (si disponible)
            if (performance.memory) {
                const usedJSHeapSize = performance.memory.usedJSHeapSize;
                const totalJSHeapSize = performance.memory.totalJSHeapSize;
                this.memoryUsage = (usedJSHeapSize / totalJSHeapSize) * 100;
            }

            // Vérifier les statistiques WebRTC
            if (this.videoManager && this.videoManager.peerConnections) {
                for (const [participantId, pc] of this.videoManager.peerConnections) {
                    const stats = await pc.getStats();
                    this.analyzeRTCStats(stats);
                }
            }

            // Vérifier l'inactivité
            const inactiveTime = Date.now() - this.lastActivityTime;
            this.isUserActive = inactiveTime < this.thresholds.inactivityTime;

        } catch (error) {
            console.error('Erreur vérification performance:', error);
        }
    }

    analyzeRTCStats(stats) {
        stats.forEach(report => {
            // Analyser les frames vidéo
            if (report.type === 'outbound-rtp' && report.kind === 'video') {
                const framesPerSecond = report.framesPerSecond || 30;
                this.frameRate = framesPerSecond;
                
                // Frames perdues
                if (report.framesDropped) {
                    this.droppedFrames = report.framesDropped;
                }
            }

            // Analyser l'utilisation CPU (approximation via encoding)
            if (report.type === 'outbound-rtp' && report.mediaType === 'video') {
                if (report.totalEncodeTime && report.framesEncoded) {
                    // Temps d'encodage moyen par frame
                    const avgEncodeTime = report.totalEncodeTime / report.framesEncoded;
                    // Estimation CPU (plus le temps est long, plus le CPU est sollicité)
                    this.cpuUsage = Math.min(100, avgEncodeTime * 100);
                }
            }
        });
    }

    optimizeIfNeeded() {
        const shouldOptimize = this.shouldOptimize();
        
        if (shouldOptimize) {
            this.applyOptimizations();
        } else if (this.optimizationMode !== 'normal' && this.canRelaxOptimization()) {
            this.relaxOptimizations();
        }
    }

    shouldOptimize() {
        // CPU élevé
        if (this.cpuUsage > this.thresholds.cpuHigh) {
            return true;
        }

        // Mémoire élevée
        if (this.memoryUsage > this.thresholds.memoryHigh) {
            return true;
        }

        // FPS trop bas
        if (this.frameRate < this.thresholds.frameRateLow) {
            return true;
        }

        // Utilisateur inactif
        if (!this.isUserActive) {
            return true;
        }

        return false;
    }

    canRelaxOptimization() {
        return this.cpuUsage < this.thresholds.cpuHigh * 0.7 &&
               this.memoryUsage < this.thresholds.memoryHigh * 0.7 &&
               this.frameRate > this.thresholds.frameRateLow * 1.5 &&
               this.isUserActive;
    }

    async applyOptimizations() {
        let newMode = 'normal';

        // Déterminer le niveau d'optimisation nécessaire
        if (this.cpuUsage > this.thresholds.cpuCritical || !this.isUserActive) {
            newMode = 'ultra-economy';
        } else if (this.cpuUsage > this.thresholds.cpuHigh) {
            newMode = 'economy';
        }

        if (newMode === this.optimizationMode) return;

        console.log(`🔧 Optimisation: passage en mode ${newMode}`);
        console.log(`   CPU: ${this.cpuUsage.toFixed(1)}%`);
        console.log(`   FPS: ${this.frameRate.toFixed(1)}`);
        console.log(`   Actif: ${this.isUserActive}`);

        this.optimizationMode = newMode;
        await this.applyCompressionSettings(newMode);

        // Notifier l'utilisateur
        this.notifyOptimization(newMode);
    }

    async relaxOptimizations() {
        console.log('✓ Performance améliorée, passage en mode normal');
        this.optimizationMode = 'normal';
        await this.applyCompressionSettings('normal');
    }

    async applyCompressionSettings(mode) {
        const settings = this.compressionSettings[mode];
        
        if (!this.videoManager || !this.videoManager.peerConnections) return;

        // Appliquer à toutes les connexions
        for (const [participantId, pc] of this.videoManager.peerConnections) {
            try {
                const senders = pc.getSenders();
                
                for (const sender of senders) {
                    if (sender.track && sender.track.kind === 'video') {
                        const parameters = sender.getParameters();
                        
                        if (!parameters.encodings) {
                            parameters.encodings = [{}];
                        }

                        // Appliquer les paramètres de compression
                        parameters.encodings[0].maxBitrate = settings.maxBitrate;
                        parameters.encodings[0].scaleResolutionDownBy = settings.scaleResolutionDownBy;
                        
                        // Ajuster le frame rate
                        if (mode === 'ultra-economy') {
                            parameters.encodings[0].maxFramerate = 15;
                        } else if (mode === 'economy') {
                            parameters.encodings[0].maxFramerate = 24;
                        } else {
                            parameters.encodings[0].maxFramerate = 30;
                        }

                        await sender.setParameters(parameters);
                        console.log(`✓ Compression appliquée: ${mode} (${settings.maxBitrate / 1000}kbps)`);
                    }
                }
            } catch (error) {
                console.error('Erreur application compression:', error);
            }
        }

        // Réduire la résolution locale si ultra-economy et inactif
        if (mode === 'ultra-economy' && !this.isUserActive) {
            this.pauseLocalVideo();
        } else if (this.videoManager.isVideoActive) {
            this.resumeLocalVideo();
        }
    }

    pauseLocalVideo() {
        if (this.videoManager && this.videoManager.localStream) {
            const videoTrack = this.videoManager.localStream.getVideoTracks()[0];
            if (videoTrack && videoTrack.enabled) {
                videoTrack.enabled = false;
                console.log('⏸️ Vidéo locale mise en pause (inactivité)');
            }
        }
    }

    resumeLocalVideo() {
        if (this.videoManager && this.videoManager.localStream && this.videoManager.isVideoActive) {
            const videoTrack = this.videoManager.localStream.getVideoTracks()[0];
            if (videoTrack && !videoTrack.enabled) {
                videoTrack.enabled = true;
                console.log('▶️ Vidéo locale reprise');
            }
        }
    }

    setupActivityDetection() {
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        
        const updateActivity = () => {
            this.lastActivityTime = Date.now();
            if (!this.isUserActive) {
                this.isUserActive = true;
                // Réactiver si nécessaire
                if (this.optimizationMode === 'ultra-economy') {
                    this.optimizeIfNeeded();
                }
            }
        };

        // Throttle pour éviter trop d'événements
        let throttleTimer = null;
        const throttledUpdate = () => {
            if (throttleTimer) return;
            throttleTimer = setTimeout(() => {
                updateActivity();
                throttleTimer = null;
            }, 1000);
        };

        events.forEach(event => {
            document.addEventListener(event, throttledUpdate, { passive: true });
        });
    }

    notifyOptimization(mode) {
        const messages = {
            'economy': '⚡ Mode économie activé (CPU élevé)',
            'ultra-economy': '🔋 Mode ultra-économie (optimisation maximale)',
            'normal': '✓ Mode normal rétabli'
        };

        const message = messages[mode];
        if (message && window.LinguaMeet) {
            LinguaMeet.showSystemMessage(message, 'info');
        }
    }

    getPerformanceMetrics() {
        return {
            cpu: this.cpuUsage.toFixed(1) + '%',
            memory: this.memoryUsage.toFixed(1) + '%',
            fps: this.frameRate.toFixed(1),
            droppedFrames: this.droppedFrames,
            mode: this.optimizationMode,
            active: this.isUserActive
        };
    }

    displayPerformanceOverlay() {
        // Créer un overlay de performance pour le débogage
        let overlay = document.getElementById('performance-overlay');
        
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'performance-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(0, 0, 0, 0.8);
                color: #00ff00;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 12px;
                z-index: 10000;
                pointer-events: none;
            `;
            document.body.appendChild(overlay);
        }

        const metrics = this.getPerformanceMetrics();
        overlay.innerHTML = `
            <div>CPU: ${metrics.cpu}</div>
            <div>MEM: ${metrics.memory}</div>
            <div>FPS: ${metrics.fps}</div>
            <div>MODE: ${metrics.mode}</div>
            <div>ACTIVE: ${metrics.active ? 'YES' : 'NO'}</div>
        `;
    }

    // Activer/désactiver l'overlay de débogage
    toggleDebugOverlay() {
        this.debugOverlay = !this.debugOverlay;
        
        if (this.debugOverlay) {
            this.debugInterval = setInterval(() => {
                this.displayPerformanceOverlay();
            }, 1000);
        } else {
            if (this.debugInterval) {
                clearInterval(this.debugInterval);
            }
            const overlay = document.getElementById('performance-overlay');
            if (overlay) {
                overlay.remove();
            }
        }
    }

    cleanup() {
        this.stopMonitoring();
        if (this.debugInterval) {
            clearInterval(this.debugInterval);
        }
        const overlay = document.getElementById('performance-overlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

// Export global
if (typeof window !== 'undefined') {
    window.PerformanceOptimizer = PerformanceOptimizer;
}
