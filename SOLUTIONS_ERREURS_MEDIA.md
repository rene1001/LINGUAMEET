# Solutions aux Erreurs Médias - LinguaMeet

## 🔴 Erreurs Rencontrées

### 1. **NotReadableError: Device in use**
```
Erreur d'accès aux médias: NotReadableError: Device in use
```

**Cause** : Votre caméra ou microphone est déjà utilisé par une autre application.

**Solutions** :
1. ✅ **Fermez les autres applications** qui utilisent la caméra/micro :
   - Zoom, Microsoft Teams, Skype
   - Google Meet dans d'autres onglets
   - Applications de streaming (OBS, etc.)
   - Applications de vidéoconférence

2. ✅ **Redémarrez votre navigateur** complètement (fermez tous les onglets)

3. ✅ **Vérifiez les permissions** :
   - Chrome : `chrome://settings/content/camera` et `chrome://settings/content/microphone`
   - Edge : `edge://settings/content/camera` et `edge://settings/content/microphone`
   - Firefox : Paramètres → Vie privée et sécurité → Permissions

4. ✅ **Sous Windows** :
   - Paramètres → Confidentialité → Caméra/Microphone
   - Vérifiez que "Autoriser les applications à accéder à votre caméra" est activé

---

### 2. **Erreur code 403 (content.js)**
```
Uncaught (in promise) {name: 'i', httpError: false, code: 403}
```

**Cause** : Extension de navigateur qui interfère (traducteur, ad blocker, etc.)

**Solutions** :
1. ✅ **Mode incognito** : Testez en mode navigation privée (les extensions sont désactivées)
2. ✅ **Désactivez temporairement les extensions** :
   - Extensions de traduction (Google Translate, DeepL)
   - Bloqueurs de publicité (AdBlock, uBlock Origin)
   - Extensions de confidentialité
3. ✅ **Ajoutez une exception** dans vos extensions pour `localhost` ou `127.0.0.1`

---

### 3. **The deferred DOM Node could not be resolved**
```
The deferred DOM Node could not be resolved to a valid node
```

**Cause** : Avertissement des outils de développement (DevTools), peut être ignoré

**Solution** : Aucune action requise, c'est juste un avertissement

---

## 🛠️ Améliorations Appliquées

### ✅ Gestion d'erreurs améliorée
- Messages d'erreur spécifiques selon le type d'erreur
- Affichage convivial dans l'interface (pas d'alert JavaScript)
- Durée d'affichage adaptable

### ✅ Paramètres audio/vidéo optimisés
```javascript
video: { width: { ideal: 1280 }, height: { ideal: 720 } }
audio: { 
    echoCancellation: true,
    noiseSuppression: true,
    autoGainControl: true
}
```

### ✅ Détection des problèmes
- Vérification de la disponibilité des API
- Détection du type d'erreur exact
- Messages d'aide contextuel

---

## 📋 Checklist de Dépannage

Avant de lancer une réunion :

- [ ] Aucune autre application n'utilise la caméra/micro
- [ ] Permissions accordées dans le navigateur
- [ ] Permissions système activées (Windows/Mac)
- [ ] Extensions problématiques désactivées
- [ ] Test en mode incognito si besoin
- [ ] Navigateur à jour (Chrome, Edge, Firefox recommandés)

---

## 🚀 Test Rapide

1. **Fermer toutes les applications** de visio
2. **Ouvrir un nouvel onglet** et aller sur `chrome://settings/content/camera`
3. **Vérifier** que LinguaMeet est autorisé
4. **Recharger** la page de réunion
5. **Autoriser** l'accès quand le navigateur le demande

---

## 💡 Conseils

### Navigateurs Recommandés
- ✅ **Google Chrome** (version 90+)
- ✅ **Microsoft Edge** (version 90+)
- ✅ **Firefox** (version 88+)
- ⚠️ Safari (support limité de WebRTC)

### Connexion HTTPS
Pour la production, assurez-vous d'utiliser HTTPS. Les API WebRTC sont restreintes en HTTP (sauf localhost).

---

## 📞 Support

Si le problème persiste après avoir suivi ces étapes :

1. Vérifiez les logs complets dans la console du navigateur (F12)
2. Testez avec un autre navigateur
3. Vérifiez que votre caméra/micro fonctionne dans d'autres applications
4. Redémarrez votre ordinateur

---

*Dernière mise à jour : 23 octobre 2025*
