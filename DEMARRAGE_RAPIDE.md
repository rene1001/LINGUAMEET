# 🚀 Démarrage Rapide - LinguaMeet v2.0

## ⚡ Lancement en 3 Étapes

### 1. Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Créer un super utilisateur (optionnel)
```bash
python manage.py createsuperuser
```

### 3. Lancer le serveur
```bash
python manage.py runserver
```

**Ouvrez** : http://localhost:8000

---

## 👤 Première Connexion

### Option A : Créer un compte
1. Vous serez automatiquement redirigé vers `/login/`
2. Cliquez sur **"S'inscrire"**
3. Remplissez le formulaire
4. Cliquez **"S'inscrire"**
5. ✅ Vous êtes connecté et sur la page d'accueil !

### Option B : Utiliser le super utilisateur
1. Connectez-vous avec les identifiants du superuser
2. ✅ Accès direct à la page d'accueil

---

## 🎬 Créer Votre Première Réunion

### Étape 1 : Page d'accueil
```
✅ Vous êtes sur la nouvelle interface style Google Meet
```

### Étape 2 : Créer
1. Cliquez sur **"Nouvelle réunion"** (bouton violet)
2. Remplissez :
   - Nom : "Ma première réunion"
   - Langue : Français
3. Cliquez **"Créer la réunion"**

### Étape 3 : Configuration
1. Entrez votre nom
2. Choisissez :
   - **Langue parlée** : Français
   - **Langue d'écoute** : Anglais (ou autre)
3. Cliquez **"Rejoindre"**

### Étape 4 : Permissions
```
⚠️ Le navigateur demande l'accès :
- Microphone : Autoriser ✅
- Caméra : Autoriser ✅
```

### Étape 5 : Dans la salle
```
✅ Vous voyez :
- Votre vidéo
- Contrôles (Micro, Caméra, Partage d'écran)
- Liste des participants
```

---

## 🎤 Tester la Traduction Audio

### Parler :
1. Votre micro est **ACTIF** par défaut (bouton vert)
2. Parlez en français : "Bonjour, comment ça va ?"
3. Les autres entendent en anglais (si c'est leur langue)

### Écouter :
1. Les autres parlent en leur langue
2. Vous entendez en français (ou votre langue choisie)

---

## 🖥️ Tester le Partage d'Écran

### Démarrer :
1. Cliquez sur **"Partager l'écran"** (bouton bleu)
2. Fenêtre système s'ouvre
3. Choisissez :
   - ⬜ **Écran complet**
   - 🪟 **Fenêtre** (ex: navigateur, Word)
   - 🌐 **Onglet Chrome**
4. Cliquez **"Partager"**

### Résultat :
```
✅ Votre vidéo montre maintenant votre écran
✅ Les autres participants voient votre écran en temps réel
✅ Notification : "Partage d'écran activé"
```

### Arrêter :
1. Cliquez sur **"Arrêter le partage"** (bouton rouge)
2. OU cliquez sur la notification système
3. ✅ Retour automatique à votre caméra

---

## 👥 Tester avec Plusieurs Participants

### Méthode 1 : Plusieurs onglets (même navigateur)
```bash
1. Ouvrez un 2ème onglet
2. Connectez-vous avec un autre compte (ou inscrivez-vous)
3. Rejoignez la même salle avec le code UUID
4. ✅ Vous voyez maintenant 2 participants !
```

### Méthode 2 : Plusieurs navigateurs
```bash
1. Ouvrez Chrome + Firefox
2. Connectez-vous sur chacun
3. Rejoignez la même salle
4. ✅ Test de compatibilité cross-browser
```

### Méthode 3 : Plusieurs appareils
```bash
1. Sur votre PC : Créez une salle
2. Sur votre téléphone : Rejoignez avec le code
3. ✅ Test mobile + desktop
```

---

## 🎯 Fonctionnalités à Tester

### ✅ Authentification
- [ ] S'inscrire avec un nouveau compte
- [ ] Se connecter
- [ ] Se déconnecter
- [ ] Redirection automatique

### ✅ Page d'accueil
- [ ] Design moderne affiché
- [ ] Bouton "Nouvelle réunion" fonctionne
- [ ] Modal s'ouvre
- [ ] Création de salle fonctionne

### ✅ Réunion
- [ ] Rejoindre une salle
- [ ] Voir sa propre vidéo
- [ ] Activer/désactiver micro
- [ ] Activer/désactiver caméra
- [ ] Voir les autres participants

### ✅ Traduction audio
- [ ] Parler en français → Traduit en anglais
- [ ] Entendre en français (les autres parlent en anglais)
- [ ] Transcription en temps réel

### ✅ Partage d'écran
- [ ] Partager écran complet
- [ ] Partager une fenêtre
- [ ] Partager un onglet
- [ ] Les autres voient l'écran
- [ ] Arrêter le partage
- [ ] Retour à la caméra

---

## 🐛 Problèmes Courants

### "Page not found" sur la page d'accueil
```bash
Solution :
python manage.py migrate
python manage.py runserver
```

### Pas de son/vidéo
```bash
Solution :
1. Vérifier permissions navigateur (icône 🔒 dans barre d'adresse)
2. Autoriser micro et caméra
3. Tester avec chrome://settings/content
```

### Partage d'écran ne fonctionne pas
```bash
Solution :
1. Utiliser Chrome ou Edge (recommandé)
2. Firefox : Fonctionne mais parfois limité
3. Safari : Support partiel
```

### CSS cassé / pas de style
```bash
Solution :
python manage.py collectstatic --noinput
Ctrl + F5 (vider cache navigateur)
```

### Erreur "CSRF token missing"
```bash
Solution :
1. Vérifier que {% csrf_token %} est dans les formulaires
2. Effacer cookies du navigateur
3. Redémarrer serveur
```

---

## 📊 Vérifications Techniques

### Base de données
```bash
python manage.py shell

>>> from django.contrib.auth.models import User
>>> User.objects.count()  # Nombre d'utilisateurs
>>> 
>>> from conference.models import Room
>>> Room.objects.count()  # Nombre de salles créées
```

### Fichiers statiques
```bash
python manage.py findstatic video-webrtc.js
# Doit afficher le chemin du fichier
```

### URLs disponibles
```bash
python manage.py show_urls

# Doit afficher :
# /                     conference:home
# /login/              conference:login
# /register/           conference:register
# /logout/             conference:logout
# ...
```

---

## 🎨 Personnalisation (Optionnel)

### Changer les couleurs
**Fichier** : `conference/templates/conference/home_meet.html`

```css
/* Ligne ~40 : Gradient principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Remplacer par vos couleurs */
background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
```

### Changer le logo
**Fichier** : `conference/templates/conference/home_meet.html`

```html
<!-- Ligne ~150 : Logo -->
<span class="brand-icon">🌍</span>

<!-- Remplacer par votre emoji/image -->
<span class="brand-icon">🚀</span>
```

### Changer le nom
**Fichier** : Tous les templates

```html
LinguaMeet → VotreNom
```

---

## 📈 Monitoring

### Logs en temps réel
```bash
python manage.py runserver

# Regardez les messages :
# 🎓 Pipeline GRATUIT Premium activé
# ✅ Google Speech-to-Text initialisé
# ✅ Gemini API initialisé
# ✅ Google Text-to-Speech initialisé
```

### Console navigateur (F12)
```javascript
// Messages importants :
"Salle de conférence initialisée avec vidéo"
"Flux vidéo local initialisé"
"Connexion WebSocket établie"
"Partage d'écran activé"
```

---

## 🌟 C'est Parti !

Vous avez maintenant :
- ✅ Interface moderne style Google Meet
- ✅ Authentification complète
- ✅ Traduction audio en temps réel
- ✅ Partage d'écran WebRTC
- ✅ Visioconférence multilingue

**Bon test ! 🚀**

---

## 📞 Besoin d'Aide ?

1. **Documentation complète** : `NOUVELLES_FONCTIONNALITES.md`
2. **Configuration gratuite** : `README_ETUDIANT.md`
3. **API recommendations** : `API_RECOMMENDATIONS.md`

**LinguaMeet v2.0 - Prêt à l'emploi !** 🎉
