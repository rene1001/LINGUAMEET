# 🚀 Guide d'intégration rapide - Nouvelles fonctionnalités LinguaMeet

## ⚡ Mise en route en 5 minutes

### Étape 1 : Ajouter les scripts dans room.html

Localisez votre template `templates/conference/room.html` et ajoutez ces scripts **avant la balise `</body>`** :

```html
<!-- Juste avant </body> -->

<!-- 1. Détection d'activité vocale -->
<script src="{% static 'js/voice-activity-detector.js' %}"></script>

<!-- 2. Historique des traductions -->
<script src="{% static 'js/translation-history.js' %}"></script>

<!-- 3. Améliorations de conférence -->
<script src="{% static 'js/conference-enhancements.js' %}"></script>

<!-- 4. Initialisation -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    // Attendre que videoManager soit initialisé
    if (typeof videoManager !== 'undefined' && window.conferenceEnhancements) {
        conferenceEnhancements.initialize(videoManager, PARTICIPANT_ID);
        console.log('✓ Améliorations de conférence activées');
    }
});
</script>
</body>
</html>
```

---

### Étape 2 : Intégrer avec l'historique de traduction

Dans votre code qui gère les traductions WebSocket (probablement dans `room-integration.js` ou `room.js`), ajoutez :

```javascript
// Quand vous recevez une traduction du WebSocket
function handleTranslatedAudio(message) {
    // ... votre code existant ...
    
    // NOUVEAU : Ajouter à l'historique
    if (window.translationHistory) {
        translationHistory.addTranslation({
            speakerName: message.participant_name,
            speakerId: message.participant_id,
            originalText: message.original_text,
            translatedText: message.translated_text,
            originalLanguage: message.original_language || 'fr',
            targetLanguage: message.target_language || 'en'
        });
        
        // Mettre à jour le badge avec le nombre total
        const count = translationHistory.history.length;
        conferenceEnhancements.updateHistoryBadge(count);
    }
}
```

---

### Étape 3 : Intégrer l'indicateur de traduction

Lorsque vous **démarrez** une traduction :

```javascript
// Avant d'envoyer l'audio au serveur
function sendAudioForTranslation(audioData) {
    // Afficher l'indicateur
    if (window.translationHistory) {
        translationHistory.showTranslationIndicator();
    }
    
    // Envoyer l'audio
    websocket.send(JSON.stringify({
        type: 'audio_data',
        audio_data: audioData
    }));
}
```

Lorsque vous **recevez** la traduction :

```javascript
// Quand la traduction arrive
function onTranslationReceived(data) {
    // Masquer l'indicateur
    if (window.translationHistory) {
        translationHistory.hideTranslationIndicator();
    }
    
    // ... traiter la traduction ...
}
```

---

### Étape 4 : Gérer le toggle du microphone

Dans votre fonction de toggle du micro, ajoutez :

```javascript
function toggleMicrophone() {
    micActive = !micActive;
    
    // ... votre code existant ...
    
    // NOUVEAU : Notifier l'indicateur de micro
    if (window.conferenceEnhancements) {
        conferenceEnhancements.onMicrophoneToggle(micActive);
    }
}
```

---

### Étape 5 : Ajouter un lien vers la page de test

Dans `templates/conference/join_room.html` ou `select_language.html`, ajoutez un lien vers la page de test :

```html
<div class="mb-3">
    <a href="{% url 'conference:device_test' room.id %}" class="btn btn-outline-primary">
        <i class="fas fa-vial me-2"></i>
        Tester mon matériel
    </a>
</div>
```

Ou créez un bouton avant de rejoindre :

```html
<div class="alert alert-info">
    <i class="fas fa-info-circle me-2"></i>
    Première fois ? 
    <a href="{% url 'conference:device_test' room.id %}">
        Testez votre caméra et micro
    </a>
</div>
```

---

## 🎨 Personnalisation des styles

### Modifier les couleurs de l'indicateur de qualité

Dans `video-webrtc.js`, ligne ~220, modifiez :

```javascript
const qualityConfig = {
    'excellent': { text: 'Excellente', color: '#1e8e3e', icon: '●●●●' },
    'good': { text: 'Bonne', color: '#1e8e3e', icon: '●●●○' },
    'fair': { text: 'Moyenne', color: '#f9ab00', icon: '●●○○' },
    'poor': { text: 'Faible', color: '#ea4335', icon: '●○○○' }
};
```

### Modifier la taille de l'historique

Dans `translation-history.js`, ligne ~8 :

```javascript
this.maxHistory = 500; // Modifier cette valeur (ex: 1000)
```

---

## 🔧 Configuration avancée

### Régler la sensibilité du détecteur de voix

Dans votre code d'initialisation :

```javascript
// Après l'initialisation
if (window.conferenceEnhancements.voiceDetector) {
    // Seuil : 0-100 (30 par défaut)
    // Plus bas = plus sensible
    conferenceEnhancements.voiceDetector.setThreshold(25);
}
```

### Désactiver certaines fonctionnalités

```javascript
// Initialisation personnalisée
const enhancements = new ConferenceEnhancements();

// Initialiser SANS certaines fonctionnalités
enhancements.videoManager = videoManager;
enhancements.participantId = PARTICIPANT_ID;

// Activer seulement ce que vous voulez
enhancements.createVideoQualitySelector();  // Sélecteur qualité
enhancements.setupTranslationHistory();     // Historique seulement
// Ne pas appeler setupVoiceActivityDetection() si non désiré
```

---

## 📱 Responsive et Mobile

### Adapter pour mobile

Ajoutez dans vos styles CSS :

```css
@media (max-width: 768px) {
    /* Réduire la taille du panneau d'historique */
    .history-panel {
        width: 100%;
        right: -100%;
    }
    
    /* Ajuster le bouton d'historique */
    .history-toggle-btn {
        bottom: 80px;
        right: 10px;
        width: 48px;
        height: 48px;
    }
    
    /* Ajuster l'indicateur de qualité */
    .connection-quality-indicator {
        font-size: 10px;
        padding: 3px 6px;
    }
}
```

---

## 🐛 Débogage

### Activer les logs détaillés

Dans la console du navigateur :

```javascript
// Voir tous les événements de détection vocale
window.addEventListener('voiceActivityStart', () => {
    console.log('🎤 Parole détectée');
});

window.addEventListener('voiceActivityStop', () => {
    console.log('🎤 Parole arrêtée');
});

// Voir l'historique complet
console.log('Historique:', translationHistory.history);

// Voir les statistiques
console.log('Stats:', translationHistory.getStatistics());
```

### Vérifier que tout fonctionne

```javascript
// Dans la console du navigateur
console.log('Détecteur vocal:', window.VoiceActivityDetector);
console.log('Historique:', window.translationHistory);
console.log('Améliorations:', window.conferenceEnhancements);
console.log('Manager vidéo:', window.videoManager);
```

---

## ✅ Checklist de vérification

- [ ] Scripts ajoutés dans room.html
- [ ] Historique intégré avec WebSocket
- [ ] Indicateur de traduction ajouté
- [ ] Toggle micro mis à jour
- [ ] Lien vers page de test ajouté
- [ ] Testé sur Chrome/Firefox
- [ ] Testé sur mobile
- [ ] Logs vérifiés dans console

---

## 🎯 Exemples d'utilisation

### Exemple 1 : Notification personnalisée quand connexion faible

```javascript
// Écouter les changements de qualité
if (window.videoManager) {
    const originalMethod = videoManager.updateConnectionQualityIndicator;
    videoManager.updateConnectionQualityIndicator = function(participantId, quality) {
        originalMethod.call(this, participantId, quality);
        
        // Action personnalisée
        if (quality === 'poor') {
            alert('⚠️ Connexion très faible ! Considérez passer en audio seul.');
        }
    };
}
```

### Exemple 2 : Export automatique en fin de session

```javascript
// Avant de quitter la salle
window.addEventListener('beforeunload', () => {
    if (confirm('Exporter l\'historique avant de quitter ?')) {
        translationHistory.exportAsText();
    }
});
```

### Exemple 3 : Statistiques en temps réel

```javascript
// Afficher les stats toutes les 30 secondes
setInterval(() => {
    const stats = translationHistory.getStatistics();
    console.log(`📊 Stats de session:
        - ${stats.total} traductions
        - ${stats.speakers.length} intervenants
        - ${stats.languages.length} langues
    `);
}, 30000);
```

---

## 🚨 Problèmes courants et solutions

### Problème : L'indicateur de micro ne s'affiche pas

**Solution** :
```javascript
// Vérifier que le flux audio existe
if (!videoManager.localStream) {
    console.error('Pas de flux audio local');
}

// Vérifier les permissions
navigator.permissions.query({name: 'microphone'}).then(result => {
    console.log('Permission micro:', result.state);
});
```

### Problème : L'historique ne se sauvegarde pas

**Solution** :
```javascript
// Vérifier localStorage disponible
try {
    localStorage.setItem('test', 'test');
    localStorage.removeItem('test');
    console.log('✓ localStorage disponible');
} catch(e) {
    console.error('❌ localStorage non disponible:', e);
}
```

### Problème : Le sélecteur de qualité ne change rien

**Solution** :
```javascript
// Vérifier que videoManager est bien passé
console.log('Video manager:', conferenceEnhancements.videoManager);

// Tester manuellement
if (videoManager) {
    videoManager.changeVideoQuality('sd').then(() => {
        console.log('✓ Qualité changée en SD');
    });
}
```

---

## 📞 Support

En cas de problème :

1. Ouvrir la console (F12)
2. Rechercher les erreurs en rouge
3. Vérifier les logs avec les emoji ✓ ou ❌
4. Copier le message d'erreur complet

---

## 🎉 C'est tout !

Vos nouvelles fonctionnalités sont maintenant prêtes à l'emploi.

**Prochaines étapes** :
1. Testez chaque fonctionnalité
2. Personnalisez selon vos besoins
3. Partagez vos retours d'expérience

Bon développement ! 🚀
