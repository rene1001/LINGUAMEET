# 🚀 Guide de Déploiement - LinguaMeet sur Google Cloud Platform

## 📋 Prérequis

1. **Compte Google Cloud Platform**
   - Projet GCP créé : `gen-lang-client-0170871086`
   - Facturation activée
   - Cloud SDK (`gcloud`) installé sur votre machine

2. **APIs Google Cloud à activer**
   - Cloud Run API
   - Cloud Build API
   - Container Registry API
   - Cloud SQL Admin API (optionnel pour PostgreSQL)

---

## 🔧 Configuration Initiale

### 1. Installer Google Cloud SDK

**Windows (PowerShell):**
```powershell
# Télécharger et installer depuis : https://cloud.google.com/sdk/docs/install
# Ou via Chocolatey :
choco install gcloudsdk
```

**Vérifier l'installation:**
```bash
gcloud --version
```

### 2. Authentification et Configuration

```bash
# Se connecter à Google Cloud
gcloud auth login

# Configurer le projet
gcloud config set project gen-lang-client-0170871086

# Configurer la région (Europe)
gcloud config set run/region europe-west1

# Authentification pour Docker
gcloud auth configure-docker
```

### 3. Activer les APIs nécessaires

```bash
# Activer toutes les APIs en une commande
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  sqladmin.googleapis.com
```

---

## 🗄️ Configuration de la Base de Données (Optionnel)

### Option A: SQLite (Gratuit - Développement uniquement)
Par défaut, l'application utilise SQLite. **Ne convient PAS pour la production** car Cloud Run est stateless.

### Option B: Cloud SQL PostgreSQL (Recommandé pour Production)

#### 1. Créer une instance Cloud SQL

```bash
# Créer une instance PostgreSQL
gcloud sql instances create linguameet-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west1 \
  --root-password=VOTRE_MOT_DE_PASSE_SECURISE

# Créer la base de données
gcloud sql databases create linguameet \
  --instance=linguameet-db

# Créer un utilisateur
gcloud sql users create linguameet-user \
  --instance=linguameet-db \
  --password=MOT_DE_PASSE_UTILISATEUR
```

#### 2. Récupérer la chaîne de connexion

```bash
# Obtenir le CONNECTION_NAME
gcloud sql instances describe linguameet-db --format='value(connectionName)'
# Format: gen-lang-client-0170871086:europe-west1:linguameet-db
```

La DATABASE_URL sera configurée dans les variables d'environnement Cloud Run.

---

## 🔑 Configuration des Variables d'Environnement

### 1. Générer une SECRET_KEY Django

**Python:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Créer un fichier `.env.production` (local uniquement)

```bash
# Copier le template
copy .env.example .env.production
```

**Contenu de `.env.production`:**
```env
# Django
SECRET_KEY=votre-secret-key-generee-ici
DEBUG=False
ALLOWED_HOSTS=linguameet-xxxxxxxxxx-ew.a.run.app,.run.app
CSRF_TRUSTED_ORIGINS=https://linguameet-xxxxxxxxxx-ew.a.run.app

# Database (si vous utilisez Cloud SQL)
DATABASE_URL=postgresql://linguameet-user:MOT_DE_PASSE@/linguameet?host=/cloudsql/gen-lang-client-0170871086:europe-west1:linguameet-db

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/google-cloud-key.json
USE_GOOGLE_CLOUD=True
```

---

## 📦 Déploiement sur Cloud Run

### Méthode 1: Déploiement Direct (Recommandé pour débuter)

#### 1. Construction et déploiement avec `gcloud`

```bash
# Se placer dans le dossier du projet
cd c:\wamp64\www\LangMeet\LINGUAMEET

# Déployer directement sur Cloud Run
gcloud run deploy linguameet \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 3600 \
  --max-instances 10 \
  --set-env-vars "DEBUG=False,USE_GOOGLE_CLOUD=True"
```

#### 2. Configurer les variables d'environnement sensibles

```bash
# Définir la SECRET_KEY (remplacer par votre clé générée)
gcloud run services update linguameet \
  --region europe-west1 \
  --update-env-vars SECRET_KEY="votre-secret-key-ici"

# Si vous utilisez Cloud SQL
gcloud run services update linguameet \
  --region europe-west1 \
  --add-cloudsql-instances gen-lang-client-0170871086:europe-west1:linguameet-db \
  --update-env-vars DATABASE_URL="postgresql://linguameet-user:PASSWORD@/linguameet?host=/cloudsql/gen-lang-client-0170871086:europe-west1:linguameet-db"
```

#### 3. Mettre à jour ALLOWED_HOSTS et CSRF_TRUSTED_ORIGINS

Après le premier déploiement, Cloud Run vous donnera une URL (ex: `https://linguameet-abc123-ew.a.run.app`).

```bash
# Récupérer l'URL du service
gcloud run services describe linguameet \
  --region europe-west1 \
  --format='value(status.url)'

# Mettre à jour les variables (remplacer par votre URL)
gcloud run services update linguameet \
  --region europe-west1 \
  --update-env-vars ALLOWED_HOSTS="linguameet-abc123-ew.a.run.app,.run.app" \
  --update-env-vars CSRF_TRUSTED_ORIGINS="https://linguameet-abc123-ew.a.run.app"
```

---

### Méthode 2: Déploiement avec Cloud Build (Production)

#### 1. Utiliser le fichier `cloudbuild.yaml`

```bash
# Soumettre le build
gcloud builds submit --config cloudbuild.yaml
```

#### 2. Configuration des variables d'environnement

Après le build, configurez les variables comme dans la Méthode 1, étape 2 et 3.

---

## 🔄 Migration de la Base de Données

Si vous utilisez Cloud SQL, vous devez exécuter les migrations Django :

### Option A: Cloud Run Job (Recommandé)

```bash
# Créer un job pour les migrations
gcloud run jobs create linguameet-migrate \
  --image gcr.io/gen-lang-client-0170871086/linguameet:latest \
  --region europe-west1 \
  --set-env-vars DATABASE_URL="postgresql://..." \
  --command python \
  --args "manage.py,migrate"

# Exécuter les migrations
gcloud run jobs execute linguameet-migrate --region europe-west1
```

### Option B: Localement via Cloud SQL Proxy

```bash
# Télécharger Cloud SQL Proxy
# https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-shell

# Démarrer le proxy
cloud-sql-proxy gen-lang-client-0170871086:europe-west1:linguameet-db

# Dans un autre terminal, exécuter les migrations
python manage.py migrate
```

---

## 🎯 Post-Déploiement

### 1. Créer un superutilisateur Django

```bash
# Via Cloud Run Job
gcloud run jobs create linguameet-createsuperuser \
  --image gcr.io/gen-lang-client-0170871086/linguameet:latest \
  --region europe-west1 \
  --set-env-vars DATABASE_URL="postgresql://..." \
  --command python \
  --args "manage.py,createsuperuser"

gcloud run jobs execute linguameet-createsuperuser --region europe-west1
```

Ou utilisez Cloud SQL Proxy (Option B ci-dessus).

### 2. Tester l'application

```bash
# Obtenir l'URL de votre application
gcloud run services describe linguameet \
  --region europe-west1 \
  --format='value(status.url)'

# Ouvrir dans le navigateur
start https://votre-url.run.app
```

### 3. Vérifier les logs

```bash
# Voir les logs en temps réel
gcloud run services logs tail linguameet --region europe-west1
```

---

## 🔄 Mises à Jour et Redéploiement

### Déploiement rapide après modifications

```bash
# Reconstruire et redéployer
gcloud run deploy linguameet \
  --source . \
  --platform managed \
  --region europe-west1
```

### Rollback en cas de problème

```bash
# Lister les révisions
gcloud run revisions list --service linguameet --region europe-west1

# Revenir à une révision précédente
gcloud run services update-traffic linguameet \
  --to-revisions REVISION_NAME=100 \
  --region europe-west1
```

---

## 💰 Gestion des Coûts

### Estimation des coûts mensuels :

- **Cloud Run** : ~0-5€/mois (petit trafic)
- **Cloud SQL (db-f1-micro)** : ~10€/mois
- **Cloud Build** : 120 minutes/jour gratuites
- **Container Registry** : ~0.5€/mois

### Optimisation :

```bash
# Réduire le nombre d'instances à 2 maximum
gcloud run services update linguameet \
  --region europe-west1 \
  --max-instances 2 \
  --min-instances 0

# Réduire la mémoire à 512 MiB
gcloud run services update linguameet \
  --region europe-west1 \
  --memory 512Mi
```

---

## 🛠️ Dépannage

### Erreur: "Permission denied"
```bash
# Vérifier les permissions
gcloud projects get-iam-policy gen-lang-client-0170871086

# Ajouter les rôles nécessaires
gcloud projects add-iam-policy-binding gen-lang-client-0170871086 \
  --member="user:VOTRE_EMAIL@gmail.com" \
  --role="roles/run.admin"
```

### Erreur: "Build failed"
```bash
# Voir les logs du build
gcloud builds list --limit 5
gcloud builds log BUILD_ID
```

### Erreur: "Container failed to start"
```bash
# Voir les logs du service
gcloud run services logs read linguameet --region europe-west1 --limit 50
```

### WebSockets ne fonctionnent pas
- Vérifiez que le timeout est suffisant (3600s)
- Cloud Run supporte les WebSockets mais avec un timeout maximum de 60 minutes

---

## 🔒 Sécurité

### Variables d'environnement sensibles

**NE JAMAIS** mettre de secrets dans le code ou `cloudbuild.yaml`. Utilisez :

#### Option A: Secret Manager (Recommandé)

```bash
# Créer un secret
echo -n "votre-secret-key" | gcloud secrets create django-secret-key \
  --data-file=- \
  --replication-policy="automatic"

# Donner l'accès à Cloud Run
gcloud secrets add-iam-policy-binding django-secret-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Utiliser dans Cloud Run
gcloud run services update linguameet \
  --region europe-west1 \
  --update-secrets=SECRET_KEY=django-secret-key:latest
```

#### Option B: Variables d'environnement (Simple)

```bash
# Définir directement (OK pour dev/test)
gcloud run services update linguameet \
  --region europe-west1 \
  --update-env-vars SECRET_KEY="votre-secret"
```

---

## 📊 Monitoring

### Activer Cloud Monitoring

```bash
# Les logs sont automatiquement dans Cloud Logging
# Accéder via : https://console.cloud.google.com/logs

# Créer des alertes personnalisées
# https://console.cloud.google.com/monitoring/alerting
```

---

## 🌐 Domaine Personnalisé

### Ajouter un domaine personnalisé

```bash
# Mapper un domaine
gcloud run domain-mappings create \
  --service linguameet \
  --domain votre-domaine.com \
  --region europe-west1

# Suivre les instructions pour configurer les DNS
```

---

## ✅ Checklist de Déploiement

- [ ] Google Cloud SDK installé et configuré
- [ ] APIs activées (Cloud Run, Cloud Build, Container Registry)
- [ ] SECRET_KEY générée et configurée
- [ ] Variables d'environnement configurées
- [ ] Base de données créée (Cloud SQL ou SQLite)
- [ ] Migrations exécutées
- [ ] Superutilisateur créé
- [ ] Application testée et fonctionnelle
- [ ] ALLOWED_HOSTS et CSRF_TRUSTED_ORIGINS mis à jour
- [ ] Logs vérifiés (pas d'erreurs)
- [ ] Coûts estimés et budget défini

---

## 📞 Support

- **Documentation Google Cloud Run** : https://cloud.google.com/run/docs
- **Django Deployment Checklist** : https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- **Console Google Cloud** : https://console.cloud.google.com/home/dashboard?project=gen-lang-client-0170871086

---

## 🚀 Commandes Rapides (TL;DR)

```bash
# Configuration initiale (une fois)
gcloud auth login
gcloud config set project gen-lang-client-0170871086
gcloud config set run/region europe-west1
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Déploiement (à chaque mise à jour)
cd c:\wamp64\www\LangMeet\LINGUAMEET
gcloud run deploy linguameet \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 3600 \
  --set-env-vars "DEBUG=False,SECRET_KEY=VOTRE_SECRET_KEY"

# Obtenir l'URL
gcloud run services describe linguameet --region europe-west1 --format='value(status.url)'
```

---

**Bonne chance avec votre déploiement ! 🎉**
