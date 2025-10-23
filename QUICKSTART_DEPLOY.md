# 🚀 Déploiement Rapide sur Google Cloud

## ⚡ Démarrage en 5 Minutes

### 1. Prérequis
- [ ] Compte Google Cloud créé
- [ ] Facturation activée
- [ ] Google Cloud SDK installé ([Télécharger](https://cloud.google.com/sdk/docs/install))

### 2. Installation de Google Cloud SDK

**Windows:**
```powershell
# Télécharger et installer depuis:
# https://cloud.google.com/sdk/docs/install

# Ou via Chocolatey:
choco install gcloudsdk
```

### 3. Déploiement Automatique (Méthode Facile) 🎯

#### Windows - Avec le script automatisé:
```powershell
# Ouvrir PowerShell dans le dossier LINGUAMEET
cd c:\wamp64\www\LangMeet\LINGUAMEET

# Exécuter le script de déploiement
.\deploy.bat

# Ou directement avec PowerShell:
.\deploy.ps1
```

Le script fait TOUT automatiquement:
- ✅ Vérifie les prérequis
- ✅ Configure Google Cloud
- ✅ Active les APIs nécessaires
- ✅ Génère une SECRET_KEY
- ✅ Construit l'image Docker
- ✅ Déploie sur Cloud Run
- ✅ Configure la sécurité
- ✅ Vous donne l'URL de l'application

### 4. Déploiement Manuel (Méthode Complète)

#### Étape 1: Configuration initiale
```bash
# Authentification
gcloud auth login

# Configurer le projet
gcloud config set project gen-lang-client-0170871086
gcloud config set run/region europe-west1

# Activer les APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

#### Étape 2: Générer une SECRET_KEY
```python
# Avec Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Étape 3: Déployer
```bash
# Déployer l'application
gcloud run deploy linguameet \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 3600 \
  --set-env-vars "DEBUG=False,SECRET_KEY=VOTRE_SECRET_KEY_ICI"
```

#### Étape 4: Obtenir l'URL
```bash
gcloud run services describe linguameet \
  --region europe-west1 \
  --format='value(status.url)'
```

#### Étape 5: Configurer la sécurité
```bash
# Remplacer VOTRE_URL par l'URL obtenue à l'étape 4
gcloud run services update linguameet \
  --region europe-west1 \
  --update-env-vars "ALLOWED_HOSTS=VOTRE_URL,.run.app" \
  --update-env-vars "CSRF_TRUSTED_ORIGINS=https://VOTRE_URL"
```

---

## 🗄️ Base de Données (Optionnel)

Par défaut, l'application utilise **SQLite** (⚠️ **ne convient PAS pour la production**).

### Utiliser Cloud SQL PostgreSQL (Recommandé):

```bash
# 1. Créer l'instance
gcloud sql instances create linguameet-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west1 \
  --root-password=MOT_DE_PASSE_SECURISE

# 2. Créer la base de données
gcloud sql databases create linguameet --instance=linguameet-db

# 3. Créer un utilisateur
gcloud sql users create linguameet-user \
  --instance=linguameet-db \
  --password=MOT_DE_PASSE_USER

# 4. Obtenir le CONNECTION_NAME
gcloud sql instances describe linguameet-db \
  --format='value(connectionName)'

# 5. Mettre à jour Cloud Run
gcloud run services update linguameet \
  --region europe-west1 \
  --add-cloudsql-instances CONNECTION_NAME \
  --update-env-vars DATABASE_URL="postgresql://linguameet-user:PASSWORD@/linguameet?host=/cloudsql/CONNECTION_NAME"

# 6. Exécuter les migrations (via Cloud SQL Proxy localement)
python manage.py migrate
```

---

## 🔄 Mises à Jour

### Redéployer après des modifications:

**Avec le script:**
```powershell
.\deploy.bat
```

**Manuellement:**
```bash
gcloud run deploy linguameet \
  --source . \
  --platform managed \
  --region europe-west1
```

---

## 📊 Commandes Utiles

### Voir les logs
```bash
gcloud run services logs tail linguameet --region europe-west1
```

### Lister les révisions
```bash
gcloud run revisions list --service linguameet --region europe-west1
```

### Rollback vers une révision précédente
```bash
gcloud run services update-traffic linguameet \
  --to-revisions REVISION_NAME=100 \
  --region europe-west1
```

### Supprimer le service
```bash
gcloud run services delete linguameet --region europe-west1
```

---

## 💰 Coûts Estimés

### Niveau Gratuit:
- **Cloud Run**: 2 millions de requêtes/mois GRATUIT
- **Cloud Build**: 120 minutes/jour GRATUIT

### Avec Cloud SQL (si utilisé):
- **Cloud SQL (db-f1-micro)**: ~10€/mois
- **Cloud Run (petit trafic)**: 0-5€/mois
- **Total**: ~10-15€/mois

### Optimiser les coûts:
```bash
# Limiter les instances
gcloud run services update linguameet \
  --region europe-west1 \
  --max-instances 2 \
  --min-instances 0

# Réduire la mémoire
gcloud run services update linguameet \
  --region europe-west1 \
  --memory 512Mi
```

---

## 🛠️ Dépannage

### Erreur: "gcloud: command not found"
- Installez Google Cloud SDK: https://cloud.google.com/sdk/docs/install
- Redémarrez votre terminal après installation

### Erreur: "Permission denied"
```bash
# Vérifier que vous êtes bien authentifié
gcloud auth list

# Se réauthentifier si nécessaire
gcloud auth login
```

### Erreur: "Build failed"
```bash
# Voir les logs du dernier build
gcloud builds list --limit 1
gcloud builds log BUILD_ID
```

### Application ne démarre pas
```bash
# Voir les logs du service
gcloud run services logs read linguameet \
  --region europe-west1 \
  --limit 50
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- **Guide complet**: [DEPLOY_GOOGLE_CLOUD.md](DEPLOY_GOOGLE_CLOUD.md)
- **Console Google Cloud**: https://console.cloud.google.com/home/dashboard?project=gen-lang-client-0170871086

---

## ✅ Checklist Rapide

- [ ] Google Cloud SDK installé
- [ ] Authentification effectuée (`gcloud auth login`)
- [ ] Projet configuré (`gcloud config set project gen-lang-client-0170871086`)
- [ ] APIs activées
- [ ] SECRET_KEY générée
- [ ] Application déployée
- [ ] URL récupérée et testée
- [ ] ALLOWED_HOSTS et CSRF_TRUSTED_ORIGINS configurés

---

**C'est tout ! Votre application est en ligne ! 🎉**

Pour toute question, consultez le guide complet dans `DEPLOY_GOOGLE_CLOUD.md`.
