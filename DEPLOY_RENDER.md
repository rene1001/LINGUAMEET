# 🚀 Déploiement sur Render.com - LinguaMeet

## ✨ Pourquoi Render ?

- ✅ **100% GRATUIT** pour les petits projets
- ✅ **Aucune carte bancaire** requise
- ✅ **PostgreSQL gratuit** inclus (256 MB)
- ✅ Support **Django + WebSockets** (Daphne)
- ✅ **SSL automatique** (HTTPS)
- ✅ Déploiement en **5-10 minutes**
- ✅ **Redéploiement automatique** à chaque push Git

---

## 📋 Prérequis

1. **Compte GitHub** (pour le code source)
2. **Compte Render.com** (gratuit)

C'est tout ! 🎉

---

## 🎯 Déploiement en 4 Étapes

### **ÉTAPE 1 : Créer un Compte Render (2 minutes)**

#### 1. Aller sur Render.com

Visitez : **https://render.com**

#### 2. S'inscrire

Cliquez sur **"Get Started"** ou **"Sign Up"**

Choisissez une méthode d'inscription :
- **GitHub** (recommandé) ⭐
- Google
- Email

#### 3. Vérifier votre email

Si vous utilisez l'email, vérifiez votre boîte de réception.

✅ **Compte créé !**

---

### **ÉTAPE 2 : Pousser Votre Code sur GitHub (3 minutes)**

Si votre code n'est **pas encore sur GitHub** :

#### 1. Créer un nouveau repository sur GitHub

1. Allez sur https://github.com/new
2. Nom : `linguameet` (ou autre)
3. Visibilité : **Public** ou **Private** (les deux fonctionnent)
4. Cliquez sur **"Create repository"**

#### 2. Pousser votre code

**Dans votre terminal PowerShell** :

```powershell
# Se placer dans le dossier du projet
cd c:\wamp64\www\LangMeet\LINGUAMEET

# Initialiser Git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Préparation pour déploiement Render"

# Ajouter le repository distant (remplacez par votre URL GitHub)
git remote add origin https://github.com/VOTRE_USERNAME/linguameet.git

# Pousser le code
git branch -M main
git push -u origin main
```

✅ **Code sur GitHub !**

---

### **ÉTAPE 3 : Déployer sur Render (5 minutes)**

#### 1. Se connecter à Render

Allez sur : **https://dashboard.render.com**

#### 2. Créer un nouveau Blueprint

1. Cliquez sur **"New +"** (en haut à droite)
2. Sélectionnez **"Blueprint"**

#### 3. Connecter votre Repository GitHub

1. Cliquez sur **"Connect a repository"**
2. Autorisez Render à accéder à GitHub (si demandé)
3. Sélectionnez le repository **`linguameet`**
4. Cliquez sur **"Connect"**

#### 4. Détecter le Blueprint

Render va automatiquement détecter le fichier `render.yaml` et afficher :
- ✅ Service Web : **linguameet**
- ✅ Base de données : **linguameet-db**

#### 5. Appliquer le Blueprint

1. Vérifiez que tout est correct
2. Cliquez sur **"Apply"** ou **"Create Resources"**

#### 6. Attendre le Déploiement

Render va maintenant :
- 📦 Créer la base de données PostgreSQL
- 🏗️ Builder l'application (exécuter `build.sh`)
- 🚀 Démarrer le serveur (exécuter `start.sh`)

**Temps estimé** : 5-10 minutes

Vous pouvez suivre les logs en temps réel dans le dashboard.

✅ **Déploiement en cours !**

---

### **ÉTAPE 4 : Vérifier et Tester (2 minutes)**

#### 1. Obtenir l'URL de votre application

Une fois le déploiement terminé, Render vous donnera une URL du type :

```
https://linguameet.onrender.com
```

#### 2. Ouvrir votre application

Cliquez sur l'URL ou ouvrez-la dans votre navigateur.

#### 3. Créer un superutilisateur Django (optionnel)

Pour accéder à l'admin Django :

1. Dans le dashboard Render, allez dans votre service **linguameet**
2. Cliquez sur **"Shell"** (dans le menu de gauche)
3. Exécutez :

```bash
python manage.py createsuperuser
```

4. Suivez les instructions (nom, email, mot de passe)

#### 4. Tester les fonctionnalités

- ✅ Accueil : https://votre-app.onrender.com
- ✅ Admin : https://votre-app.onrender.com/admin
- ✅ WebSockets : Testez une vidéoconférence

✅ **Application en ligne !**

---

## 🎉 C'est Terminé !

Votre application **LinguaMeet** est maintenant en ligne et accessible publiquement !

**URL** : `https://linguameet.onrender.com` (ou similaire)

---

## 🔄 Mises à Jour Automatiques

### Redéploiement automatique

Chaque fois que vous **poussez du code** sur GitHub (branch `main`), Render va **automatiquement** :
1. Télécharger le nouveau code
2. Exécuter `build.sh`
3. Redémarrer l'application

```powershell
# Faire des modifications dans votre code
# ...

# Commit et push
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin main

# Render redéploie automatiquement ! 🚀
```

---

## 📊 Limitations du Niveau Gratuit

### Ce qui est inclus (GRATUIT) :

- ✅ **750 heures/mois** de service web
- ✅ **PostgreSQL 256 MB** (suffisant pour commencer)
- ✅ **100 GB de bande passante/mois**
- ✅ **SSL/HTTPS automatique**
- ✅ **Déploiements illimités**

### Limitations :

- ⚠️ **Mise en veille** après 15 minutes d'inactivité
  - Le service redémarre au premier accès (peut prendre 30 secondes)
  - Pas de problème pour un projet étudiant !

- ⚠️ **Stockage limité** (256 MB pour PostgreSQL)
  - Suffisant pour ~1000 utilisateurs

### Comment éviter la mise en veille ?

**Option 1** : Utiliser un service de "ping" gratuit
- https://uptimerobot.com (gratuit)
- Configure un ping toutes les 10 minutes

**Option 2** : Passer au plan payant (7$/mois)
- Pas de mise en veille
- Plus de ressources

---

## 🛠️ Commandes Utiles

### Voir les logs en temps réel

1. Dashboard Render → Votre service
2. Onglet **"Logs"**

### Accéder à la console (Shell)

1. Dashboard Render → Votre service
2. Onglet **"Shell"**
3. Tapez vos commandes Django :

```bash
# Migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Shell Django
python manage.py shell
```

### Redéployer manuellement

1. Dashboard Render → Votre service
2. Cliquez sur **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🗄️ Base de Données PostgreSQL

### Accéder aux informations de connexion

1. Dashboard Render → **Databases** → **linguameet-db**
2. Vous verrez :
   - **Host**
   - **Port**
   - **Database**
   - **Username**
   - **Password**
   - **Connection String**

### Se connecter avec un client PostgreSQL

Utilisez un client comme :
- **pgAdmin** (gratuit)
- **DBeaver** (gratuit)
- **psql** (ligne de commande)

### Faire un backup

```bash
# Dans le Shell Render
pg_dump $DATABASE_URL > backup.sql
```

---

## 🔒 Variables d'Environnement

### Ajouter/Modifier des variables

1. Dashboard Render → Votre service
2. Onglet **"Environment"**
3. Cliquez sur **"Add Environment Variable"**

Variables automatiquement configurées :
- ✅ `SECRET_KEY` (générée automatiquement)
- ✅ `DEBUG` = False
- ✅ `DATABASE_URL` (PostgreSQL)
- ✅ `RENDER_EXTERNAL_HOSTNAME` (votre domaine)

---

## 🌐 Domaine Personnalisé (Optionnel)

### Ajouter votre propre domaine

1. Dashboard Render → Votre service
2. Onglet **"Settings"**
3. Section **"Custom Domains"**
4. Cliquez sur **"Add Custom Domain"**
5. Entrez votre domaine (ex: `linguameet.com`)
6. Configurez les DNS selon les instructions

✅ SSL/HTTPS automatique même pour les domaines personnalisés !

---

## 💰 Passer au Plan Payant (Optionnel)

Si vous voulez **plus de ressources** :

### Plans disponibles :

- **Starter** : 7$/mois
  - Pas de mise en veille
  - Plus de mémoire (512 MB)
  
- **Standard** : 25$/mois
  - Encore plus de ressources
  - Support prioritaire

### Comment upgrader :

1. Dashboard Render → Votre service
2. Onglet **"Settings"**
3. Section **"Instance Type"**
4. Sélectionnez le plan souhaité

---

## 🐛 Dépannage

### Erreur : "Build failed"

**Vérifier les logs** :
1. Dashboard → Logs
2. Recherchez l'erreur dans `build.sh`

**Causes communes** :
- Dépendance manquante dans `requirements.txt`
- Erreur de syntaxe Python

### Erreur : "Application timeout"

**Solution** :
- Vérifiez que Daphne démarre correctement
- Consultez les logs de démarrage

### Erreur de base de données

**Vérifier** :
- La base de données est bien créée
- `DATABASE_URL` est bien configurée
- Les migrations ont été exécutées

**Forcer les migrations** :
```bash
# Shell Render
python manage.py migrate --run-syncdb
```

### L'application est lente au démarrage

**Normal !** Sur le plan gratuit :
- Mise en veille après 15 min d'inactivité
- Redémarrage au premier accès (30 secondes)

**Solutions** :
- Utiliser UptimeRobot pour ping régulier
- Passer au plan payant

---

## 📚 Ressources

- **Documentation Render** : https://render.com/docs
- **Dashboard Render** : https://dashboard.render.com
- **Status Render** : https://status.render.com
- **Support** : support@render.com

---

## ✅ Checklist Post-Déploiement

- [ ] Application accessible via l'URL Render
- [ ] WebSockets fonctionnent (test de vidéoconférence)
- [ ] Base de données PostgreSQL opérationnelle
- [ ] Admin Django accessible
- [ ] Superutilisateur créé
- [ ] Fichiers statiques servis correctement
- [ ] SSL/HTTPS actif
- [ ] Logs vérifiés (pas d'erreurs)

---

## 🎯 Prochaines Étapes

1. **Tester toutes les fonctionnalités**
2. **Ajouter du contenu** (créer des salles, utilisateurs, etc.)
3. **Partager l'URL** avec vos amis/collègues
4. **Monitorer l'utilisation** via le dashboard Render
5. **(Optionnel)** Configurer un domaine personnalisé
6. **(Optionnel)** Mettre en place UptimeRobot

---

## 🆘 Besoin d'Aide ?

- **Documentation** : https://render.com/docs/deploy-django
- **Community Forum** : https://community.render.com
- **Stack Overflow** : Tag `render.com`

---

**Félicitations ! Votre application est en ligne ! 🎉🚀**

---

## 📝 Résumé Ultra-Rapide

```bash
# 1. Pousser sur GitHub
git init
git add .
git commit -m "Deploy to Render"
git remote add origin https://github.com/USERNAME/linguameet.git
git push -u origin main

# 2. Sur Render.com
# - New + → Blueprint
# - Connect repository
# - Apply

# 3. Attendre 5-10 minutes

# 4. Votre app est en ligne !
# https://linguameet.onrender.com
```

**C'est tout ! 🎊**
