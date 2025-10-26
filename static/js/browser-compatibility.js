// LinguaMeet - Détection et correction de compatibilité navigateurs

class BrowserCompatibility {
    constructor() {
        this.browser = this.detectBrowser();
        this.features = {};
        this.issues = [];
        this.warnings = [];
    }

    detectBrowser() {
        const userAgent = navigator.userAgent;
        let browserName = 'Unknown';
        let browserVersion = 'Unknown';
        let engine = 'Unknown';

        // Détection Chrome
        if (/Chrome/.test(userAgent) && !/Edge|Edg/.test(userAgent)) {
            browserName = 'Chrome';
            const match = userAgent.match(/Chrome\/(\d+)/);
            if (match) browserVersion = match[1];
            engine = 'Blink';
        }
        // Détection Edge
        else if (/Edg/.test(userAgent)) {
            browserName = 'Edge';
            const match = userAgent.match(/Edg\/(\d+)/);
            if (match) browserVersion = match[1];
            engine = 'Blink';
        }
        // Détection Firefox
        else if (/Firefox/.test(userAgent)) {
            browserName = 'Firefox';
            const match = userAgent.match(/Firefox\/(\d+)/);
            if (match) browserVersion = match[1];
            engine = 'Gecko';
        }
        // Détection Safari
        else if (/Safari/.test(userAgent) && !/Chrome/.test(userAgent)) {
            browserName = 'Safari';
            const match = userAgent.match(/Version\/(\d+)/);
            if (match) browserVersion = match[1];
            engine = 'WebKit';
        }
        // Détection Opera
        else if (/OPR/.test(userAgent)) {
            browserName = 'Opera';
            const match = userAgent.match(/OPR\/(\d+)/);
            if (match) browserVersion = match[1];
            engine = 'Blink';
        }

        return {
            name: browserName,
            version: parseInt(browserVersion),
            engine: engine,
            userAgent: userAgent,
            platform: navigator.platform,
            isMobile: /Mobile|Android|iPhone|iPad/.test(userAgent)
        };
    }

    checkCompatibility() {
        console.log(`🔍 Vérification compatibilité: ${this.browser.name} ${this.browser.version}`);

        // Vérifier toutes les fonctionnalités
        this.checkWebRTC();
        this.checkMediaDevices();
        this.checkWebAudio();
        this.checkWebSocket();
        this.checkES6Features();
        this.checkStorageAPIs();
        this.checkNotifications();

        // Afficher le rapport
        this.displayCompatibilityReport();

        return {
            compatible: this.issues.length === 0,
            issues: this.issues,
            warnings: this.warnings,
            features: this.features
        };
    }

    checkWebRTC() {
        this.features.webrtc = {
            supported: false,
            RTCPeerConnection: false,
            getUserMedia: false,
            getDisplayMedia: false
        };

        // RTCPeerConnection
        if (window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection) {
            this.features.webrtc.RTCPeerConnection = true;
            window.RTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
        } else {
            this.issues.push({
                feature: 'RTCPeerConnection',
                severity: 'critical',
                message: 'WebRTC non supporté - vidéoconférence impossible'
            });
        }

        // getUserMedia
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            this.features.webrtc.getUserMedia = true;
        } else if (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia) {
            // Polyfill pour anciennes versions
            navigator.mediaDevices = navigator.mediaDevices || {};
            navigator.mediaDevices.getUserMedia = (constraints) => {
                const getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
                return new Promise((resolve, reject) => {
                    getUserMedia.call(navigator, constraints, resolve, reject);
                });
            };
            this.features.webrtc.getUserMedia = true;
            this.warnings.push({
                feature: 'getUserMedia',
                message: 'API getUserMedia ancienne - polyfill appliqué'
            });
        } else {
            this.issues.push({
                feature: 'getUserMedia',
                severity: 'critical',
                message: 'Accès caméra/micro impossible'
            });
        }

        // getDisplayMedia (partage d'écran)
        if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
            this.features.webrtc.getDisplayMedia = true;
        } else {
            this.warnings.push({
                feature: 'getDisplayMedia',
                message: 'Partage d\'écran non supporté'
            });
        }

        this.features.webrtc.supported = this.features.webrtc.RTCPeerConnection && this.features.webrtc.getUserMedia;

        // Recommandations spécifiques par navigateur
        if (this.browser.name === 'Safari' && this.browser.version < 11) {
            this.issues.push({
                feature: 'Safari',
                severity: 'high',
                message: 'Safari < 11 a un support WebRTC limité. Mettez à jour vers Safari 11+'
            });
        }

        if (this.browser.name === 'Firefox' && this.browser.version < 55) {
            this.issues.push({
                feature: 'Firefox',
                severity: 'high',
                message: 'Firefox < 55 a un support WebRTC incomplet. Mettez à jour vers Firefox 55+'
            });
        }
    }

    checkMediaDevices() {
        this.features.mediaDevices = {
            enumerateDevices: false,
            getSupportedConstraints: false
        };

        if (navigator.mediaDevices) {
            if (typeof navigator.mediaDevices.enumerateDevices === 'function') {
                this.features.mediaDevices.enumerateDevices = true;
            } else {
                this.warnings.push({
                    feature: 'enumerateDevices',
                    message: 'Impossible de lister les périphériques audio/vidéo'
                });
            }

            if (typeof navigator.mediaDevices.getSupportedConstraints === 'function') {
                this.features.mediaDevices.getSupportedConstraints = true;
            }
        }
    }

    checkWebAudio() {
        this.features.webAudio = {
            supported: false,
            AudioContext: false,
            createMediaStreamSource: false
        };

        if (window.AudioContext || window.webkitAudioContext) {
            this.features.webAudio.AudioContext = true;
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            
            // Tester createMediaStreamSource
            try {
                const tempContext = new AudioContext();
                if (typeof tempContext.createMediaStreamSource === 'function') {
                    this.features.webAudio.createMediaStreamSource = true;
                }
                tempContext.close();
            } catch (e) {
                console.warn('Erreur test Web Audio:', e);
            }

            this.features.webAudio.supported = true;
        } else {
            this.issues.push({
                feature: 'Web Audio API',
                severity: 'medium',
                message: 'Détection vocale et effets audio non disponibles'
            });
        }
    }

    checkWebSocket() {
        this.features.webSocket = {
            supported: !!window.WebSocket
        };

        if (!window.WebSocket) {
            this.issues.push({
                feature: 'WebSocket',
                severity: 'critical',
                message: 'WebSocket non supporté - communication temps réel impossible'
            });
        }
    }

    checkES6Features() {
        this.features.es6 = {
            promises: typeof Promise !== 'undefined',
            arrow: false,
            classes: false,
            async: false,
            fetch: typeof fetch !== 'undefined'
        };

        // Test arrow functions
        try {
            eval('(() => {})');
            this.features.es6.arrow = true;
        } catch (e) {
            this.warnings.push({
                feature: 'Arrow Functions',
                message: 'Fonctions fléchées non supportées - navigation peut être ralentie'
            });
        }

        // Test classes
        try {
            eval('class Test {}');
            this.features.es6.classes = true;
        } catch (e) {
            this.issues.push({
                feature: 'ES6 Classes',
                severity: 'high',
                message: 'Classes ES6 non supportées - application peut ne pas fonctionner'
            });
        }

        // Test async/await
        try {
            eval('async function test() { await Promise.resolve(); }');
            this.features.es6.async = true;
        } catch (e) {
            this.issues.push({
                feature: 'Async/Await',
                severity: 'high',
                message: 'Async/await non supporté - fonctionnalités limitées'
            });
        }

        if (!this.features.es6.promises) {
            this.issues.push({
                feature: 'Promises',
                severity: 'critical',
                message: 'Promises non supportées - application ne fonctionnera pas'
            });
        }

        if (!this.features.es6.fetch) {
            this.warnings.push({
                feature: 'Fetch API',
                message: 'Fetch API non supportée - utilisation de XMLHttpRequest'
            });
        }
    }

    checkStorageAPIs() {
        this.features.storage = {
            localStorage: false,
            sessionStorage: false,
            indexedDB: false
        };

        // localStorage
        try {
            localStorage.setItem('test', 'test');
            localStorage.removeItem('test');
            this.features.storage.localStorage = true;
        } catch (e) {
            this.warnings.push({
                feature: 'localStorage',
                message: 'localStorage non disponible - paramètres non sauvegardés'
            });
        }

        // sessionStorage
        try {
            sessionStorage.setItem('test', 'test');
            sessionStorage.removeItem('test');
            this.features.storage.sessionStorage = true;
        } catch (e) {
            this.warnings.push({
                feature: 'sessionStorage',
                message: 'sessionStorage non disponible'
            });
        }

        // IndexedDB
        this.features.storage.indexedDB = !!window.indexedDB;
    }

    checkNotifications() {
        this.features.notifications = {
            supported: 'Notification' in window,
            permission: 'Notification' in window ? Notification.permission : 'denied'
        };
    }

    displayCompatibilityReport() {
        if (this.issues.length === 0 && this.warnings.length === 0) {
            console.log('✅ Navigateur entièrement compatible !');
            return;
        }

        console.group('🔍 Rapport de compatibilité');
        console.log(`Navigateur: ${this.browser.name} ${this.browser.version}`);
        console.log(`Moteur: ${this.browser.engine}`);
        console.log(`Plateforme: ${this.browser.platform}`);
        console.log(`Mobile: ${this.browser.isMobile ? 'Oui' : 'Non'}`);

        if (this.issues.length > 0) {
            console.group('❌ Problèmes détectés:');
            this.issues.forEach(issue => {
                const icon = issue.severity === 'critical' ? '🛑' : issue.severity === 'high' ? '⚠️' : '⚡';
                console.log(`${icon} [${issue.feature}] ${issue.message}`);
            });
            console.groupEnd();
        }

        if (this.warnings.length > 0) {
            console.group('⚠️ Avertissements:');
            this.warnings.forEach(warning => {
                console.log(`⚠️ [${warning.feature}] ${warning.message}`);
            });
            console.groupEnd();
        }

        console.groupEnd();

        // Afficher notification si problèmes critiques
        if (this.issues.some(i => i.severity === 'critical')) {
            this.showCompatibilityWarning();
        }
    }

    showCompatibilityWarning() {
        const warning = document.createElement('div');
        warning.className = 'browser-compatibility-warning';
        warning.innerHTML = `
            <div class="compatibility-warning-content">
                <i class="fas fa-exclamation-triangle"></i>
                <div>
                    <strong>Navigateur non compatible</strong>
                    <p>Votre navigateur (${this.browser.name} ${this.browser.version}) ne supporte pas toutes les fonctionnalités nécessaires.</p>
                    <p class="compatibility-recommendation">
                        ${this.getRecommendation()}
                    </p>
                </div>
                <button class="compatibility-warning-details" onclick="browserCompatibility.showDetailedReport()">
                    Détails
                </button>
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            .browser-compatibility-warning {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #ea4335 0%, #ff6b6b 100%);
                color: white;
                padding: 16px;
                z-index: 10002;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }

            .compatibility-warning-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                gap: 16px;
            }

            .compatibility-warning-content i {
                font-size: 32px;
            }

            .compatibility-warning-content strong {
                display: block;
                font-size: 16px;
                margin-bottom: 4px;
            }

            .compatibility-warning-content p {
                margin: 4px 0;
                font-size: 14px;
                opacity: 0.95;
            }

            .compatibility-recommendation {
                margin-top: 8px;
                font-weight: 600;
            }

            .compatibility-warning-details {
                padding: 8px 16px;
                border: 2px solid white;
                background: transparent;
                color: white;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                white-space: nowrap;
                transition: all 0.2s;
            }

            .compatibility-warning-details:hover {
                background: white;
                color: #ea4335;
            }
        `;
        document.head.appendChild(style);

        document.body.insertBefore(warning, document.body.firstChild);
    }

    getRecommendation() {
        if (this.browser.name === 'Safari' && this.browser.version < 11) {
            return 'Mettez à jour vers Safari 11 ou utilisez Chrome/Firefox.';
        }
        if (this.browser.name === 'Firefox' && this.browser.version < 55) {
            return 'Mettez à jour vers Firefox 55+ ou utilisez Chrome.';
        }
        if (this.browser.name === 'Chrome' && this.browser.version < 60) {
            return 'Mettez à jour vers Chrome 60+ pour une meilleure expérience.';
        }
        if (this.browser.name === 'Edge' && this.browser.version < 79) {
            return 'Mettez à jour vers Edge 79+ (basé sur Chromium).';
        }
        return 'Utilisez Chrome 60+, Firefox 55+, Safari 11+ ou Edge 79+.';
    }

    showDetailedReport() {
        const modal = document.createElement('div');
        modal.className = 'compatibility-modal';
        modal.innerHTML = `
            <div class="compatibility-modal-content">
                <div class="compatibility-modal-header">
                    <h2>Rapport de compatibilité détaillé</h2>
                    <button onclick="this.closest('.compatibility-modal').remove()">&times;</button>
                </div>
                <div class="compatibility-modal-body">
                    <h3>Informations navigateur</h3>
                    <table>
                        <tr><td>Nom:</td><td>${this.browser.name}</td></tr>
                        <tr><td>Version:</td><td>${this.browser.version}</td></tr>
                        <tr><td>Moteur:</td><td>${this.browser.engine}</td></tr>
                        <tr><td>Plateforme:</td><td>${this.browser.platform}</td></tr>
                        <tr><td>Mobile:</td><td>${this.browser.isMobile ? 'Oui' : 'Non'}</td></tr>
                    </table>

                    ${this.issues.length > 0 ? `
                        <h3>Problèmes (${this.issues.length})</h3>
                        <ul class="compatibility-issues">
                            ${this.issues.map(issue => `
                                <li class="issue-${issue.severity}">
                                    <strong>${issue.feature}</strong>: ${issue.message}
                                </li>
                            `).join('')}
                        </ul>
                    ` : '<p class="success">✅ Aucun problème détecté</p>'}

                    ${this.warnings.length > 0 ? `
                        <h3>Avertissements (${this.warnings.length})</h3>
                        <ul class="compatibility-warnings">
                            ${this.warnings.map(warning => `
                                <li><strong>${warning.feature}</strong>: ${warning.message}</li>
                            `).join('')}
                        </ul>
                    ` : ''}

                    <h3>Fonctionnalités supportées</h3>
                    <div class="features-grid">
                        ${this.generateFeaturesTable()}
                    </div>
                </div>
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            .compatibility-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10003;
            }

            .compatibility-modal-content {
                background: white;
                border-radius: 12px;
                max-width: 800px;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            }

            .compatibility-modal-header {
                padding: 20px;
                border-bottom: 1px solid #dadce0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .compatibility-modal-header h2 {
                margin: 0;
                font-size: 20px;
            }

            .compatibility-modal-header button {
                background: none;
                border: none;
                font-size: 28px;
                cursor: pointer;
                color: #5f6368;
            }

            .compatibility-modal-body {
                padding: 20px;
            }

            .compatibility-modal-body h3 {
                margin: 20px 0 12px 0;
                font-size: 16px;
                color: #202124;
            }

            .compatibility-modal-body table {
                width: 100%;
                border-collapse: collapse;
            }

            .compatibility-modal-body table td {
                padding: 8px;
                border-bottom: 1px solid #f8f9fa;
            }

            .compatibility-modal-body table td:first-child {
                font-weight: 600;
                width: 120px;
            }

            .compatibility-issues, .compatibility-warnings {
                list-style: none;
                padding: 0;
            }

            .compatibility-issues li, .compatibility-warnings li {
                padding: 12px;
                margin-bottom: 8px;
                border-radius: 6px;
                background: #f8f9fa;
            }

            .compatibility-issues .issue-critical {
                background: #fce8e6;
                border-left: 4px solid #ea4335;
            }

            .compatibility-issues .issue-high {
                background: #fef7e0;
                border-left: 4px solid #f9ab00;
            }

            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 8px;
            }

            .feature-item {
                padding: 12px;
                border-radius: 6px;
                background: #f8f9fa;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .feature-supported { background: #e6f4ea; color: #1e8e3e; }
            .feature-unsupported { background: #fce8e6; color: #ea4335; }

            .success {
                color: #1e8e3e;
                font-weight: 600;
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(modal);
    }

    generateFeaturesTable() {
        let html = '';

        // WebRTC
        html += this.featureItem('WebRTC', this.features.webrtc?.supported);
        html += this.featureItem('getUserMedia', this.features.webrtc?.getUserMedia);
        html += this.featureItem('Partage écran', this.features.webrtc?.getDisplayMedia);
        
        // Web Audio
        html += this.featureItem('Web Audio', this.features.webAudio?.supported);
        
        // WebSocket
        html += this.featureItem('WebSocket', this.features.webSocket?.supported);
        
        // ES6
        html += this.featureItem('Promises', this.features.es6?.promises);
        html += this.featureItem('Async/Await', this.features.es6?.async);
        html += this.featureItem('Fetch API', this.features.es6?.fetch);
        
        // Storage
        html += this.featureItem('localStorage', this.features.storage?.localStorage);
        html += this.featureItem('IndexedDB', this.features.storage?.indexedDB);

        return html;
    }

    featureItem(name, supported) {
        const className = supported ? 'feature-supported' : 'feature-unsupported';
        const icon = supported ? '✓' : '✗';
        return `<div class="feature-item ${className}"><span>${name}</span><span>${icon}</span></div>`;
    }
}

// Créer instance globale
const browserCompatibility = new BrowserCompatibility();

// Export
if (typeof window !== 'undefined') {
    window.BrowserCompatibility = BrowserCompatibility;
    window.browserCompatibility = browserCompatibility;
}
