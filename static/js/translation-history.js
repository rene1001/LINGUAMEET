// LinguaMeet - Gestion de l'historique et export des traductions

class TranslationHistory {
    constructor() {
        this.history = [];
        this.maxHistory = 500;
        this.roomId = null;
        this.participantId = null;
        this.isTranslating = false;
        this.translationIndicator = null;
    }

    initialize(roomId, participantId) {
        this.roomId = roomId;
        this.participantId = participantId;
        this.createTranslationIndicator();
        this.loadHistoryFromStorage();
    }

    createTranslationIndicator() {
        // Créer l'indicateur "Traduction en cours..."
        const indicator = document.createElement('div');
        indicator.id = 'translation-indicator';
        indicator.className = 'translation-indicator';
        indicator.innerHTML = `
            <div class="translation-spinner">
                <div class="spinner-dot"></div>
                <div class="spinner-dot"></div>
                <div class="spinner-dot"></div>
            </div>
            <span class="translation-text">Traduction en cours...</span>
        `;

        // Appliquer les styles
        const style = document.createElement('style');
        style.textContent = `
            .translation-indicator {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(102, 126, 234, 0.95);
                color: white;
                padding: 12px 20px;
                border-radius: 24px;
                display: none;
                align-items: center;
                gap: 10px;
                z-index: 9999;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);
                animation: slideInRight 0.3s ease;
            }

            .translation-indicator.active {
                display: flex;
            }

            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            .translation-spinner {
                display: flex;
                gap: 4px;
            }

            .spinner-dot {
                width: 8px;
                height: 8px;
                background: white;
                border-radius: 50%;
                animation: spinnerBounce 1.4s infinite ease-in-out both;
            }

            .spinner-dot:nth-child(1) {
                animation-delay: -0.32s;
            }

            .spinner-dot:nth-child(2) {
                animation-delay: -0.16s;
            }

            @keyframes spinnerBounce {
                0%, 80%, 100% {
                    transform: scale(0);
                    opacity: 0.5;
                }
                40% {
                    transform: scale(1);
                    opacity: 1;
                }
            }

            .translation-text {
                font-size: 14px;
                font-weight: 500;
            }

            .history-panel {
                position: fixed;
                right: -450px;
                top: 70px;
                bottom: 100px;
                width: 450px;
                background: white;
                box-shadow: -2px 0 10px rgba(0, 0, 0, 0.3);
                transition: right 0.3s ease;
                z-index: 1000;
                display: flex;
                flex-direction: column;
            }

            .history-panel.open {
                right: 0;
            }

            .history-header {
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .history-header h3 {
                margin: 0;
                font-size: 18px;
                font-weight: 600;
            }

            .history-close {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background 0.2s;
            }

            .history-close:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            .history-controls {
                padding: 15px 20px;
                background: #f8f9fa;
                border-bottom: 1px solid #dadce0;
                display: flex;
                gap: 10px;
            }

            .history-btn {
                flex: 1;
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
            }

            .history-btn-export {
                background: #667eea;
                color: white;
            }

            .history-btn-export:hover {
                background: #5568d3;
            }

            .history-btn-clear {
                background: white;
                color: #5f6368;
                border: 1px solid #dadce0;
            }

            .history-btn-clear:hover {
                background: #f8f9fa;
            }

            .history-content {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }

            .history-item {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
                animation: historyItemSlide 0.3s ease;
            }

            @keyframes historyItemSlide {
                from {
                    opacity: 0;
                    transform: translateX(20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            .history-item-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }

            .history-item-speaker {
                font-weight: 600;
                color: #202124;
                font-size: 14px;
            }

            .history-item-time {
                font-size: 11px;
                color: #5f6368;
            }

            .history-item-text {
                margin-bottom: 8px;
            }

            .history-item-original {
                color: #5f6368;
                font-size: 13px;
                margin-bottom: 5px;
            }

            .history-item-translated {
                color: #202124;
                font-size: 14px;
                font-weight: 500;
            }

            .history-item-languages {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }

            .history-item-lang-badge {
                font-size: 11px;
                padding: 3px 8px;
                border-radius: 12px;
                background: white;
                color: #667eea;
                font-weight: 500;
            }

            .history-empty {
                text-align: center;
                padding: 40px 20px;
                color: #5f6368;
            }

            .history-empty i {
                font-size: 48px;
                color: #dadce0;
                margin-bottom: 15px;
            }

            .history-search {
                padding: 15px 20px;
                background: white;
                border-bottom: 1px solid #dadce0;
            }

            .history-search input {
                width: 100%;
                padding: 10px 12px;
                border: 2px solid #dadce0;
                border-radius: 6px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.3s;
            }

            .history-search input:focus {
                border-color: #667eea;
            }
        `;

        if (!document.getElementById('translation-history-styles')) {
            style.id = 'translation-history-styles';
            document.head.appendChild(style);
        }

        document.body.appendChild(indicator);
        this.translationIndicator = indicator;
    }

    showTranslationIndicator() {
        if (this.translationIndicator) {
            this.translationIndicator.classList.add('active');
            this.isTranslating = true;
        }
    }

    hideTranslationIndicator() {
        if (this.translationIndicator) {
            this.translationIndicator.classList.remove('active');
            this.isTranslating = false;
        }
    }

    addTranslation(data) {
        const translation = {
            id: Date.now() + Math.random(),
            timestamp: new Date(),
            speakerName: data.speakerName || 'Inconnu',
            speakerId: data.speakerId,
            originalText: data.originalText,
            translatedText: data.translatedText,
            originalLanguage: data.originalLanguage,
            targetLanguage: data.targetLanguage
        };

        this.history.unshift(translation);

        // Limiter la taille de l'historique
        if (this.history.length > this.maxHistory) {
            this.history = this.history.slice(0, this.maxHistory);
        }

        this.saveHistoryToStorage();
        this.updateHistoryPanel();

        return translation;
    }

    saveHistoryToStorage() {
        try {
            const key = `linguameet_history_${this.roomId}`;
            localStorage.setItem(key, JSON.stringify(this.history));
        } catch (error) {
            console.warn('Impossible de sauvegarder l\'historique:', error);
        }
    }

    loadHistoryFromStorage() {
        try {
            const key = `linguameet_history_${this.roomId}`;
            const stored = localStorage.getItem(key);
            if (stored) {
                this.history = JSON.parse(stored);
                // Reconvertir les timestamps en objets Date
                this.history.forEach(item => {
                    item.timestamp = new Date(item.timestamp);
                });
            }
        } catch (error) {
            console.warn('Impossible de charger l\'historique:', error);
            this.history = [];
        }
    }

    clearHistory() {
        if (confirm('Voulez-vous vraiment effacer tout l\'historique des traductions ?')) {
            this.history = [];
            this.saveHistoryToStorage();
            this.updateHistoryPanel();
        }
    }

    exportAsText() {
        if (this.history.length === 0) {
            alert('Aucune traduction à exporter');
            return;
        }

        let text = `=== Historique des traductions - LinguaMeet ===\n`;
        text += `Salle: ${this.roomId}\n`;
        text += `Date: ${new Date().toLocaleString('fr-FR')}\n`;
        text += `Total: ${this.history.length} traductions\n\n`;
        text += '='.repeat(60) + '\n\n';

        this.history.forEach((item, index) => {
            text += `[${item.timestamp.toLocaleTimeString('fr-FR')}] ${item.speakerName}\n`;
            text += `Original (${item.originalLanguage}): ${item.originalText}\n`;
            text += `Traduit (${item.targetLanguage}): ${item.translatedText}\n\n`;
        });

        this.downloadFile(text, `linguameet_traductions_${this.roomId}_${Date.now()}.txt`, 'text/plain');
    }

    exportAsJSON() {
        if (this.history.length === 0) {
            alert('Aucune traduction à exporter');
            return;
        }

        const data = {
            roomId: this.roomId,
            exportDate: new Date().toISOString(),
            totalTranslations: this.history.length,
            translations: this.history
        };

        const json = JSON.stringify(data, null, 2);
        this.downloadFile(json, `linguameet_traductions_${this.roomId}_${Date.now()}.json`, 'application/json');
    }

    exportAsCSV() {
        if (this.history.length === 0) {
            alert('Aucune traduction à exporter');
            return;
        }

        let csv = 'Horodatage,Intervenant,Langue origine,Texte original,Langue cible,Texte traduit\n';

        this.history.forEach(item => {
            const row = [
                item.timestamp.toLocaleString('fr-FR'),
                item.speakerName,
                item.originalLanguage,
                `"${item.originalText.replace(/"/g, '""')}"`,
                item.targetLanguage,
                `"${item.translatedText.replace(/"/g, '""')}"`
            ].join(',');
            csv += row + '\n';
        });

        this.downloadFile(csv, `linguameet_traductions_${this.roomId}_${Date.now()}.csv`, 'text/csv');
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    createHistoryPanel() {
        const panel = document.createElement('div');
        panel.id = 'history-panel';
        panel.className = 'history-panel';
        panel.innerHTML = `
            <div class="history-header">
                <h3><i class="fas fa-history me-2"></i>Historique des traductions</h3>
                <button class="history-close" onclick="translationHistory.togglePanel()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="history-search">
                <input type="text" id="history-search-input" placeholder="Rechercher dans l'historique...">
            </div>
            <div class="history-controls">
                <button class="history-btn history-btn-export" onclick="translationHistory.showExportMenu()">
                    <i class="fas fa-download"></i> Exporter
                </button>
                <button class="history-btn history-btn-clear" onclick="translationHistory.clearHistory()">
                    <i class="fas fa-trash"></i> Effacer
                </button>
            </div>
            <div class="history-content" id="history-content">
                <!-- Les éléments d'historique seront ajoutés ici -->
            </div>
        `;

        document.body.appendChild(panel);

        // Ajouter un événement de recherche
        document.getElementById('history-search-input').addEventListener('input', (e) => {
            this.filterHistory(e.target.value);
        });

        this.updateHistoryPanel();
    }

    togglePanel() {
        const panel = document.getElementById('history-panel');
        if (!panel) {
            this.createHistoryPanel();
            setTimeout(() => {
                document.getElementById('history-panel').classList.add('open');
            }, 10);
        } else {
            panel.classList.toggle('open');
        }
    }

    updateHistoryPanel() {
        const content = document.getElementById('history-content');
        if (!content) return;

        if (this.history.length === 0) {
            content.innerHTML = `
                <div class="history-empty">
                    <i class="fas fa-inbox"></i>
                    <p>Aucune traduction dans l'historique</p>
                </div>
            `;
            return;
        }

        content.innerHTML = this.history.map(item => `
            <div class="history-item">
                <div class="history-item-header">
                    <span class="history-item-speaker">${item.speakerName}</span>
                    <span class="history-item-time">${item.timestamp.toLocaleTimeString('fr-FR')}</span>
                </div>
                <div class="history-item-text">
                    <div class="history-item-original">${item.originalText}</div>
                    <div class="history-item-translated">${item.translatedText}</div>
                </div>
                <div class="history-item-languages">
                    <span class="history-item-lang-badge">${item.originalLanguage} → ${item.targetLanguage}</span>
                </div>
            </div>
        `).join('');
    }

    filterHistory(query) {
        const content = document.getElementById('history-content');
        if (!content) return;

        const filtered = this.history.filter(item => 
            item.originalText.toLowerCase().includes(query.toLowerCase()) ||
            item.translatedText.toLowerCase().includes(query.toLowerCase()) ||
            item.speakerName.toLowerCase().includes(query.toLowerCase())
        );

        if (filtered.length === 0) {
            content.innerHTML = `
                <div class="history-empty">
                    <i class="fas fa-search"></i>
                    <p>Aucun résultat pour "${query}"</p>
                </div>
            `;
            return;
        }

        content.innerHTML = filtered.map(item => `
            <div class="history-item">
                <div class="history-item-header">
                    <span class="history-item-speaker">${item.speakerName}</span>
                    <span class="history-item-time">${item.timestamp.toLocaleTimeString('fr-FR')}</span>
                </div>
                <div class="history-item-text">
                    <div class="history-item-original">${item.originalText}</div>
                    <div class="history-item-translated">${item.translatedText}</div>
                </div>
                <div class="history-item-languages">
                    <span class="history-item-lang-badge">${item.originalLanguage} → ${item.targetLanguage}</span>
                </div>
            </div>
        `).join('');
    }

    showExportMenu() {
        const menu = confirm('Choisir le format d\'export:\n\nOK = Texte (.txt)\nAnnuler = Voir plus d\'options');
        
        if (menu) {
            this.exportAsText();
        } else {
            const choice = prompt('Choisir le format:\n1 = Texte (.txt)\n2 = JSON (.json)\n3 = CSV (.csv)', '1');
            switch(choice) {
                case '1':
                    this.exportAsText();
                    break;
                case '2':
                    this.exportAsJSON();
                    break;
                case '3':
                    this.exportAsCSV();
                    break;
            }
        }
    }

    getStatistics() {
        return {
            total: this.history.length,
            languages: [...new Set(this.history.map(t => t.originalLanguage))],
            speakers: [...new Set(this.history.map(t => t.speakerName))],
            startTime: this.history.length > 0 ? this.history[this.history.length - 1].timestamp : null,
            endTime: this.history.length > 0 ? this.history[0].timestamp : null
        };
    }
}

// Créer une instance globale
const translationHistory = new TranslationHistory();

// Export pour utilisation globale
if (typeof window !== 'undefined') {
    window.TranslationHistory = TranslationHistory;
    window.translationHistory = translationHistory;
}
