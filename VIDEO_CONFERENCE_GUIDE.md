# 📹 Guide de la Visioconférence LinguaMeet

## Vue d'ensemble

La fonctionnalité de visioconférence a été ajoutée à LinguaMeet, permettant aux participants de se voir en temps réel tout en bénéficiant de la traduction audio multilingue.

## 🆕 Nouvelles fonctionnalités

### 1. **Flux vidéo en temps réel**
- Affichage vidéo de tous les participants
- Ratio 4:3 optimisé pour les visages
- Placeholder élégant quand la caméra est désactivée

### 2. **Contrôle de la caméra**
- Bouton toggle pour activer/désactiver la caméra
- État synchronisé avec tous les participants
- Feedback visuel en temps réel

### 3. **WebRTC peer-to-peer**
- Connexions directes entre participants
- Serveurs STUN Google pour le NAT traversal
- Signaling via WebSocket Django Channels

### 4. **Intégration transparente**
- Compatible avec la traduction audio existante
- Interface utilisateur cohérente
- Gestion automatique des permissions

## 🏗️ Architecture technique

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface utilisateur                     │
│  (room.html - Éléments <video> + Contrôles caméra/micro)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│              Couche JavaScript (Frontend)                    │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  main.js    │  │  room.js     │  │ video-webrtc.js  │  │
│  │ (Permissions)│  │ (Conférence) │  │ (WebRTC Manager) │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
│                    room-integration.js                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ WebSocket
┌──────────────────────┴──────────────────────────────────────┐
│                Backend Django (Python)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  consumers.py - ConferenceConsumer                   │   │
│  │  • Signaling WebRTC (offer/answer/ICE)              │   │
│  │  • Toggle vidéo/microphone                           │   │
│  │  • Traduction audio                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  models.py - Participant (+ video_actif)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                  Flux WebRTC P2P                             │
│  Participant A ←──────────────────────→ Participant B       │
│    (Video + Audio)         Direct         (Video + Audio)   │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Fichiers modifiés/créés

### Backend
- **`conference/models.py`** : Ajout du champ `video_actif` au modèle `Participant`
- **`conference/consumers.py`** : Ajout des handlers WebRTC (offer/answer/ICE) et toggle vidéo
- **`conference/migrations/0003_participant_video_actif.py`** : Migration de la base de données

### Frontend
- **`static/js/main.js`** : Ajout de `requestMediaPermissions()` pour audio+vidéo
- **`static/js/video-webrtc.js`** *(nouveau)* : Classe `VideoConferenceManager` pour gérer WebRTC
- **`static/js/room-integration.js`** *(nouveau)* : Intégration du manager vidéo dans `ConferenceRoom`
- **`templates/conference/room.html`** : Ajout des éléments `<video>`, styles CSS, et bouton caméra

## 🔧 Composants clés

### 1. VideoConferenceManager (video-webrtc.js)
```javascript
class VideoConferenceManager {
    - initialize() : Obtenir permissions média
    - createPeerConnection(id) : Créer connexion WebRTC
    - handleWebRTCOffer/Answer/ICE : Signaling
    - toggleVideo() : Activer/désactiver caméra
    - cleanup() : Nettoyer les ressources
}
```

### 2. Messages WebSocket
```javascript
// Toggle vidéo
{ type: 'video_toggle', active: true/false }

// Signaling WebRTC
{ type: 'webrtc_offer', target_id: '...', offer: {...} }
{ type: 'webrtc_answer', target_id: '...', answer: {...} }
{ type: 'webrtc_ice_candidate', target_id: '...', candidate: {...} }
```

### 3. Modèle Participant
```python
class Participant(models.Model):
    # ... champs existants ...
    video_actif = models.BooleanField(default=True)  # NOUVEAU
```

## 🚀 Utilisation

### Pour les utilisateurs

1. **Rejoindre une réunion**
   - Autoriser l'accès au microphone ET à la caméra
   - La vidéo démarre automatiquement

2. **Contrôles disponibles**
   - **Bouton Microphone** : Activer/désactiver l'audio
   - **Bouton Caméra** : Activer/désactiver la vidéo
   - Les deux sont indépendants

3. **Affichage**
   - Votre vidéo est en mode miroir (silencieux)
   - Les vidéos des autres participants sont en direct
   - Les traductions audio continuent de fonctionner

### Pour les développeurs

1. **Tester localement**
```bash
python manage.py runserver
# Ouvrir http://localhost:8000
# Créer/rejoindre une salle
```

2. **Tester avec plusieurs participants**
   - Ouvrir plusieurs onglets/fenêtres
   - Rejoindre la même salle avec des noms différents
   - Observer les connexions WebRTC dans la console

3. **Déboguer**
```javascript
// Console navigateur
conferenceRoom.videoManager.peerConnections  // Voir les connexions
LinguaMeet.log(message, type)  // Logs horodatés
```

## 🔒 Sécurité et permissions

### Permissions navigateur
- **Audio** : Requis pour la traduction vocale
- **Vidéo** : Requis pour la visioconférence
- Demandées au chargement de la salle

### Fallback
Si la caméra n'est pas disponible :
- L'application fonctionne en mode audio seul
- Les placeholders vidéo restent visibles
- Aucune interruption de service

## 📊 Performance

### Recommandations
- **Connexion** : Minimum 2 Mbps par participant
- **Processeur** : 2 cores minimum
- **Navigateurs supportés** :
  - Chrome 80+
  - Firefox 75+
  - Safari 13+
  - Edge 80+

### Limitations actuelles
- Pas de limite technique de participants
- Recommandé : 4-6 participants pour une performance optimale
- Chaque participant = 1 connexion P2P avec chacun des autres

## 🐛 Dépannage

### Vidéo ne s'affiche pas
1. Vérifier les permissions navigateur
2. Ouvrir la console : Chercher les erreurs WebRTC
3. Vérifier la connexion Internet (STUN servers)

### Audio fonctionne mais pas la vidéo
1. Vérifier que la caméra n'est pas utilisée par une autre app
2. Tester dans un onglet de navigation privée
3. Redémarrer le navigateur

### Connexion WebRTC échoue
1. Vérifier le firewall (ports UDP)
2. Peut nécessiter un serveur TURN pour certains réseaux
3. Consulter les logs Django

## 🔮 Améliorations futures

- [ ] Serveur TURN pour traverser tous les NAT
- [ ] Sélection de la résolution vidéo
- [ ] Mode "présentation" avec partage d'écran
- [ ] Enregistrement de session avec vidéo
- [ ] Layouts avancés (grille, focus speaker)
- [ ] Filtres et effets vidéo (arrière-plan flou)
- [ ] Statistiques de qualité (FPS, bitrate)

## 📚 Ressources

- [WebRTC API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- [Django Channels](https://channels.readthedocs.io/)
- [STUN/TURN Servers](https://www.metered.ca/tools/openrelay/)

---

**✅ Visioconférence intégrée avec succès dans LinguaMeet !**

*Développé pour améliorer l'expérience de communication multilingue* 🌍📹
