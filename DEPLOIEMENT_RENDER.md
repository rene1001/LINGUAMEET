# 🚀 Guide de Déploiement LinguaMeet sur Render

Ce guide explique comment déployer LinguaMeet sur Render.com avec PostgreSQL et le système de traduction Google Gemini.

---

## 📋 Prérequis

### 1. Compte Render
- Créez un compte gratuit sur [render.com](https://render.com)
- Connectez votre compte GitHub/GitLab

### 2. Clés API Nécessaires

#### a) Google Gemini API (Traduction)
1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créez une clé API Gemini
3. Copiez la clé (format: `AIzaSy...`)

#### b) Google Cloud Credentials (Speech-to-Text & Text-to-Speech)
1. Allez sur [Google Cloud Console](https://console.cloud.google.com)
2. Créez un projet ou sélectionnez-en un
3. Activez les APIs:
   - Google Cloud Speech-to-Text API
   - Google Cloud Text-to-Speech API
4. Créez un compte de service:
   - IAM & Admin > Comptes de service > Créer un compte de service
   - Rôles: "Speech-to-Text User" et "Text-to-Speech User"
5. Créez une clé JSON:
   - Cliquez sur le compte créé > Clés > Ajouter une clé > JSON
   - Téléchargez le fichier JSON

#### c) Encoder les Credentials en Base64
Pour Render, vous devez encoder le fichier JSON en base64:

**Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("credentials\google-cloud-key.json")) | Set-Clipboard
```

**Linux/Mac:**
```bash
base64 -w 0 credentials/google-cloud-key.json | pbcopy
```

La chaîne encodée sera copiée dans votre presse-papier.

---

## 🛠️ Déploiement Étape par Étape

### Étape 1: Préparer le Repository Git

Assurez-vous que tous les fichiers sont commités:

```bash
git add .
git commit -m "Prêt pour déploiement Render"
git push origin main
```

### Étape 2: Créer le Service sur Render

1. **Connectez-vous à Render Dashboard**
   - https://dashboard.render.com

2. **Créer un nouveau Blueprint**
   - Cliquez sur "New +" > "Blueprint"
   - Connectez votre repository GitHub/GitLab
   - Sélectionnez le repository LinguaMeet
   - Render détectera automatiquement le fichier `render.yaml`

3. **Configuration Automatique**
   - Render créera automatiquement:
     - Un service web (linguameet)
     - Une base de données PostgreSQL (linguameet-db)

### Étape 3: Configurer les Variables d'Environnement

Dans le dashboard Render, allez dans votre service > Environment:

#### Variables OBLIGATOIRES à Ajouter

| Variable | Valeur | Description |
|----------|--------|-------------|
| `ADMIN_PASSWORD` | `votre_mot_de_passe_securise` | Mot de passe admin (CHANGEZ-LE!) |
| `GEMINI_API_KEY` | `AIzaSy...` | Votre clé Gemini API |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | `[votre_base64]` | Credentials Google Cloud encodés en base64 |

#### Variables OPTIONNELLES (Déjà Configurées)

Les variables suivantes sont déjà dans `render.yaml`:
- `DEBUG=False`
- `SECRET_KEY` (auto-généré)
- `USE_FREE_PREMIUM=True`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL` (auto-configuré)

### Étape 4: Mettre à Jour CSRF_TRUSTED_ORIGINS

Une fois déployé, vous aurez une URL comme: `https://linguameet.onrender.com`

Mettez à jour la variable:
```
CSRF_TRUSTED_ORIGINS=https://votre-app.onrender.com
```

### Étape 5: Déployer

1. Cliquez sur **"Create Blueprint Instance"**
2. Render va:
   - Créer la base de données PostgreSQL
   - Builder l'application Docker
   - Exécuter les migrations
   - Créer l'utilisateur admin automatiquement
   - Démarrer le service

⏱️ **Temps de déploiement:** ~10-15 minutes

---

## ✅ Vérification du Déploiement

### 1. Vérifier les Logs

Dans Render Dashboard > Votre Service > Logs:

Vous devriez voir:
```
✅ Credentials Google Cloud configurées
🗄️  Applying migrations...
🗂️  Collecting static files...
👤 Creating admin user...
✅ Superutilisateur créé avec succès!
🚀 Starting Daphne on port 10000...
```

### 2. Tester l'Application

Ouvrez votre URL: `https://votre-app.onrender.com`

Vous devriez voir la page d'accueil LinguaMeet.

### 3. Se Connecter en tant qu'Administrateur

1. Allez sur: `https://votre-app.onrender.com/admin/`
2. Connectez-vous avec:
   - **Username:** `admin` (ou celui défini dans `ADMIN_USERNAME`)
   - **Password:** celui défini dans `ADMIN_PASSWORD`

⚠️ **IMPORTANT:** Changez ce mot de passe immédiatement après la première connexion!

---

## 🔧 Mise à Jour de l'Application

Pour mettre à jour votre application:

```bash
# 1. Faites vos modifications
git add .
git commit -m "Description des changements"
git push origin main

# 2. Render redéploiera automatiquement
```

### Redéploiement Manuel

Dans Render Dashboard:
- Allez dans votre service
- Cliquez sur "Manual Deploy" > "Deploy latest commit"

---

## 🐛 Résolution des Problèmes

### Problème 1: Erreur de Connexion à la Base de Données

**Solution:**
- Vérifiez que `DATABASE_URL` est bien configurée
- Attendez que la base PostgreSQL soit complètement initialisée (~2-3 min)

### Problème 2: Système de Traduction ne Fonctionne Pas

**Vérifications:**
1. `GEMINI_API_KEY` est correctement configurée
2. `GOOGLE_APPLICATION_CREDENTIALS_JSON` est le contenu base64 complet
3. Les APIs Google Cloud sont activées
4. Vérifiez les logs pour voir si les credentials sont créées

**Test depuis les logs:**
```
✅ Credentials Google Cloud configurées
```

### Problème 3: "Admin creation skipped"

C'est normal si l'admin existe déjà. Pour réinitialiser:

1. Connectez-vous au Shell Render:
   - Dashboard > Service > Shell
2. Exécutez:
   ```bash
   python manage.py shell
   from django.contrib.auth.models import User
   User.objects.filter(username='admin').delete()
   exit()
   ```
3. Redéployez

### Problème 4: Erreur 500 ou Page Blanche

**Vérifications:**
1. `DEBUG=False` est bien configuré
2. `ALLOWED_HOSTS` inclut votre domaine Render
3. `CSRF_TRUSTED_ORIGINS` est correct
4. Vérifiez les logs d'erreur

### Problème 5: Sessions/Connexion ne Fonctionne Pas

**Solution:** Ce problème a été corrigé dans `settings.py`:
- Sessions stockées en base de données
- Cookies sécurisés en production
- Configuration CSRF correcte

Si le problème persiste:
1. Videz le cache de votre navigateur
2. Essayez en navigation privée
3. Vérifiez que `SESSION_COOKIE_SECURE=True` en production

---

## 📊 Monitoring et Logs

### Accéder aux Logs

**Logs en Temps Réel:**
- Dashboard > Service > Logs

**Logs d'Erreur:**
- Dashboard > Service > Logs > Filter: "error"

### Métriques

Render fournit:
- Utilisation CPU
- Utilisation Mémoire
- Temps de réponse
- Nombre de requêtes

---

## 💰 Coûts

### Plan Gratuit Render

- **Web Service:** Gratuit (750h/mois, se met en veille après 15 min d'inactivité)
- **PostgreSQL:** Gratuit (90 jours, puis $7/mois)
- **Limites:**
  - 512 MB RAM
  - Partagé CPU
  - Temps de réveil: ~30 secondes

### APIs Google (Quotas Gratuits)

- **Gemini API:** 60 requêtes/minute (gratuit)
- **Google Speech-to-Text:** 60 minutes/mois (gratuit)
- **Google Text-to-Speech:** 1M caractères/mois (gratuit)

**Total: 0€/mois** (avec plan gratuit Render pendant 90 jours)

---

## 🔒 Sécurité en Production

### Checklist de Sécurité

- [ ] `DEBUG=False` en production
- [ ] Mot de passe admin changé
- [ ] `SECRET_KEY` unique et sécurisé (auto-généré par Render)
- [ ] HTTPS activé (automatique sur Render)
- [ ] Clés API stockées en variables d'environnement (jamais dans le code)
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] Base de données PostgreSQL avec backups activés

### Recommandations

1. **Changez le mot de passe admin régulièrement**
2. **Surveillez les logs pour détecter les tentatives d'accès**
3. **Activez les backups PostgreSQL** (Dashboard > Database > Backups)
4. **Utilisez des mots de passe forts** (12+ caractères)
5. **Ne partagez jamais vos clés API**

---

## 🎯 Domaine Personnalisé (Optionnel)

Pour utiliser votre propre domaine:

1. **Dans Render Dashboard:**
   - Service > Settings > Custom Domains
   - Ajoutez votre domaine

2. **Chez votre registrar:**
   - Ajoutez un enregistrement CNAME:
     ```
     CNAME @ your-app.onrender.com
     ```

3. **Mettez à jour les variables:**
   ```
   ALLOWED_HOSTS=votredomaine.com,.onrender.com,localhost
   CSRF_TRUSTED_ORIGINS=https://votredomaine.com,https://your-app.onrender.com
   ```

---

## 📞 Support

### Ressources Officielles

- **Documentation Render:** https://render.com/docs
- **Documentation Django:** https://docs.djangoproject.com
- **Documentation Gemini:** https://ai.google.dev/gemini-api/docs

### Besoin d'Aide ?

Si vous rencontrez des problèmes:
1. Vérifiez les logs Render
2. Consultez ce guide
3. Vérifiez que toutes les variables d'environnement sont correctes
4. Testez localement d'abord

---

## 🎉 Félicitations !

Votre application LinguaMeet est maintenant déployée en production ! 🚀

**URLs Importantes:**
- Application: `https://votre-app.onrender.com`
- Admin: `https://votre-app.onrender.com/admin/`
- Dashboard Render: `https://dashboard.render.com`

**Prochaines Étapes:**
1. Testez toutes les fonctionnalités
2. Créez quelques réunions de test
3. Invitez des utilisateurs
4. Surveillez les logs et les performances
5. Configurez les backups automatiques

---

**Date de dernière mise à jour:** 26 Octobre 2025  
**Version:** 1.0
