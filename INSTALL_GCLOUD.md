# 📥 Installation de Google Cloud SDK

## Le problème détecté

Le script de déploiement a échoué car **Google Cloud SDK n'est pas installé** sur votre système.

L'erreur indique :
```
gcloud : Le terme «gcloud» n'est pas reconnu comme nom d'applet de commande
```

---

## ✅ Solution : Installer Google Cloud SDK

### Option 1 : Installation Manuelle (Recommandé)

#### 1. Télécharger l'installateur

**Ouvrir le lien suivant dans votre navigateur :**
```
https://cloud.google.com/sdk/docs/install
```

Ou cliquez directement ici : [Télécharger Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

#### 2. Télécharger pour Windows

- Sélectionnez **"Windows"** dans la page
- Téléchargez le fichier `GoogleCloudSDKInstaller.exe`
- Taille : ~100 MB

#### 3. Installer

1. Double-cliquez sur `GoogleCloudSDKInstaller.exe`
2. Suivez les instructions de l'installateur
3. **Important** : Cochez "Add gcloud to PATH" (Ajouter gcloud au PATH)
4. Attendez la fin de l'installation (peut prendre 5-10 minutes)

#### 4. Redémarrer le terminal

**TRÈS IMPORTANT** : Fermez et rouvrez votre terminal PowerShell après l'installation.

#### 5. Vérifier l'installation

```powershell
gcloud --version
```

Vous devriez voir quelque chose comme :
```
Google Cloud SDK 456.0.0
bq 2.0.97
core 2023.11.01
gcloud-crc32c 1.0.0
gsutil 5.27
```

---

### Option 2 : Installation via Chocolatey (Si vous avez Chocolatey)

#### 1. Ouvrir PowerShell en Administrateur

Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"

#### 2. Installer Chocolatey (si pas déjà installé)

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### 3. Installer Google Cloud SDK

```powershell
choco install gcloudsdk -y
```

#### 4. Redémarrer le terminal

Fermez et rouvrez PowerShell.

#### 5. Vérifier

```powershell
gcloud --version
```

---

## 🔧 Configuration Initiale de Google Cloud SDK

Après l'installation, configurez Google Cloud :

### 1. Authentification

```powershell
gcloud auth login
```

Cela ouvrira votre navigateur pour vous connecter à votre compte Google.

### 2. Configurer le projet

```powershell
# Définir votre projet
gcloud config set project gen-lang-client-0170871086

# Définir la région par défaut
gcloud config set run/region europe-west1
```

### 3. Activer les APIs nécessaires

```powershell
# Activer toutes les APIs en une seule commande
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
```

---

## 🚀 Après l'installation

### Une fois Google Cloud SDK installé et configuré :

#### 1. Retourner dans le dossier de votre projet

```powershell
cd c:\wamp64\www\LangMeet\LINGUAMEET
```

#### 2. Utiliser le script de déploiement simplifié

```powershell
.\deploy_simple.ps1
```

**Ou** manuellement :

```powershell
gcloud run deploy linguameet \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 3600 \
  --set-env-vars "DEBUG=False,SECRET_KEY=VOTRE_SECRET_KEY"
```

---

## 🔍 Dépannage

### Problème : `gcloud` toujours non reconnu après installation

**Solution** :
1. Fermez **complètement** votre terminal
2. Rouvrez un nouveau terminal
3. Vérifiez à nouveau avec `gcloud --version`

Si toujours pas reconnu :

#### Vérifier le PATH manuellement

```powershell
# Voir si gcloud est dans le PATH
$env:Path -split ';' | Select-String -Pattern 'Google'
```

#### Ajouter manuellement au PATH (si nécessaire)

```powershell
# Ajouter temporairement (session actuelle uniquement)
$env:Path += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# OU ajouter de façon permanente via l'interface Windows
# Panneau de configuration → Système → Paramètres système avancés → Variables d'environnement
```

### Problème : Erreurs de permissions

**Solution** :
- Exécutez PowerShell en tant qu'administrateur
- Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"

### Problème : Firewall ou Antivirus bloque l'installation

**Solution** :
- Désactivez temporairement votre antivirus
- Ajoutez une exception pour Google Cloud SDK

---

## 📚 Ressources Officielles

- **Documentation officielle** : https://cloud.google.com/sdk/docs
- **Guide d'installation Windows** : https://cloud.google.com/sdk/docs/install#windows
- **Commandes gcloud** : https://cloud.google.com/sdk/gcloud/reference

---

## ✅ Checklist

Avant de déployer, assurez-vous que :

- [ ] Google Cloud SDK est installé (`gcloud --version` fonctionne)
- [ ] Vous êtes authentifié (`gcloud auth list` montre votre compte)
- [ ] Le projet est configuré (`gcloud config get-value project` retourne votre projet)
- [ ] Les APIs sont activées
- [ ] Vous êtes dans le bon dossier (`c:\wamp64\www\LangMeet\LINGUAMEET`)

---

## 🎯 Prochaines Étapes

Une fois Google Cloud SDK installé :

1. **Retournez dans votre projet** : `cd c:\wamp64\www\LangMeet\LINGUAMEET`
2. **Utilisez le nouveau script** : `.\deploy_simple.ps1`
3. **Suivez les instructions** du script

Le script simplifié :
- ✅ Vérifie que gcloud est installé
- ✅ Configure automatiquement votre projet
- ✅ Active les APIs
- ✅ Génère une SECRET_KEY
- ✅ Déploie votre application
- ✅ Configure la sécurité

---

**Besoin d'aide ?** Consultez la documentation officielle ou contactez le support Google Cloud.
