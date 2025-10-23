# 🚀 Guide d'Installation - Google Cloud APIs

## Configuration en 5 étapes (15 minutes)

### ✅ Étape 1 : Créer un projet Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com)
2. Cliquez sur **"Créer un projet"**
3. Nommez-le : `linguameet-translation`
4. Cliquez sur **"Créer"**

### ✅ Étape 2 : Activer les APIs nécessaires

Dans votre projet, activez ces 3 APIs :

1. **Cloud Speech-to-Text API**
   - [Lien direct](https://console.cloud.google.com/apis/library/speech.googleapis.com)
   - Cliquez sur **"Activer"**

2. **Cloud Translation API**
   - [Lien direct](https://console.cloud.google.com/apis/library/translate.googleapis.com)
   - Cliquez sur **"Activer"**

3. **Cloud Text-to-Speech API**
   - [Lien direct](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
   - Cliquez sur **"Activer"**

### ✅ Étape 3 : Créer une clé de service

1. Allez dans **"IAM et administration"** → **"Comptes de service"**
   - [Lien direct](https://console.cloud.google.com/iam-admin/serviceaccounts)

2. Cliquez sur **"Créer un compte de service"**

3. Remplissez :
   - **Nom** : `linguameet-service`
   - **ID** : `linguameet-service` (auto-généré)
   - Cliquez sur **"Créer et continuer"**

4. Attribuez les rôles :
   - Cliquez sur **"Sélectionner un rôle"**
   - Cherchez et ajoutez : `Cloud Speech Client`
   - Ajoutez aussi : `Cloud Translation API User`
   - Ajoutez aussi : `Cloud Text-to-Speech User`
   - Cliquez sur **"Continuer"** puis **"Terminé"**

5. Créer la clé JSON :
   - Cliquez sur le compte de service que vous venez de créer
   - Onglet **"Clés"**
   - **"Ajouter une clé"** → **"Créer une clé"**
   - Choisir **"JSON"**
   - Cliquez sur **"Créer"**
   - **Le fichier JSON est téléchargé automatiquement** 📥

### ✅ Étape 4 : Configurer le fichier de clé

1. **Déplacer le fichier téléchargé** dans votre projet :
   ```bash
   # Créer un dossier pour les credentials
   mkdir c:\wamp64\www\LangMeet\LINGUAMEET\credentials
   
   # Déplacer le fichier (remplacez le nom par le vôtre)
   move Downloads\linguameet-translation-*.json c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
   ```

2. **Créer/Modifier le fichier `.env`** à la racine du projet :
   ```bash
   # c:\wamp64\www\LangMeet\LINGUAMEET\.env
   
   # Google Cloud Credentials
   GOOGLE_APPLICATION_CREDENTIALS=c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
   
   # Activer Google Cloud Pipeline
   USE_GOOGLE_CLOUD=True
   ```

3. **Ajouter au .gitignore** (important pour la sécurité) :
   ```bash
   # Ajouter à .gitignore
   credentials/
   .env
   ```

### ✅ Étape 5 : Installer les dépendances Python

```bash
# Activer l'environnement virtuel
cd c:\wamp64\www\LangMeet\LINGUAMEET
.\venv\Scripts\activate

# Installer les packages Google Cloud
pip install google-cloud-speech
pip install google-cloud-translate
pip install google-cloud-texttospeech

# Installer python-dotenv pour lire .env
pip install python-dotenv
```

---

## 🧪 Tester l'installation

```bash
# Tester le pipeline
python -c "
import asyncio
import sys
sys.path.append('.')
from conference.ai_pipeline_google_cloud import GoogleCloudAudioProcessor

async def test():
    processor = GoogleCloudAudioProcessor()
    if processor.is_ready:
        print('✅ Google Cloud configuré correctement!')
        await processor.test_pipeline()
    else:
        print('❌ Problème de configuration')

asyncio.run(test())
"
```

Si vous voyez `✅ Google Cloud configuré correctement!`, c'est bon ! 🎉

---

## 🔄 Activer dans LinguaMeet

Le code est déjà prêt à basculer. Il vous suffit de :

**Méthode 1 : Variable d'environnement (recommandé)**
```bash
# Dans .env
USE_GOOGLE_CLOUD=True
```

**Méthode 2 : settings.py**
```python
# Dans linguameet_project/settings.py
USE_GOOGLE_CLOUD_AUDIO = True
```

Le système basculera automatiquement vers Google Cloud ! 🚀

---

## 💰 Quota Gratuit

Google Cloud offre un **quota gratuit mensuel** :

| Service | Quota Gratuit | Suffisant pour |
|---------|---------------|----------------|
| Speech-to-Text | 60 minutes | ~120 conversations courtes |
| Translation | 500,000 caractères | ~250 conversations |
| Text-to-Speech | 1M caractères Standard<br>100K WaveNet/Neural2 | ~500 réponses (Standard)<br>~50 réponses (Neural2) |

**Après le quota gratuit** :
- Speech-to-Text : $0.006 / 15 secondes
- Translation : $20 / 1M caractères
- TTS Neural2 : $16 / 1M caractères

### Estimation de coût réel
Pour **1000 minutes de conversation/mois** :
- Speech-to-Text : ~$40
- Translation : ~$5
- TTS Neural2 : ~$10
- **Total : ~$55/mois** (très raisonnable !)

---

## 🔒 Sécurité

### ⚠️ IMPORTANT - Ne JAMAIS commiter :
- ❌ Le fichier `.json` de credentials
- ❌ Le fichier `.env`
- ❌ Les clés API en dur dans le code

### ✅ Bonnes pratiques :
- Ajoutez `credentials/` et `.env` au `.gitignore`
- Utilisez des variables d'environnement
- Limitez les permissions du compte de service
- Activez la facturation alerts sur Google Cloud

---

## 📊 Monitoring (optionnel)

Pour surveiller votre utilisation :

1. Allez sur [Google Cloud Console](https://console.cloud.google.com)
2. **Facturation** → **Rapports**
3. Vous verrez l'utilisation de chaque API en temps réel

Configurez des **alertes de budget** :
1. **Facturation** → **Budgets et alertes**
2. Créer un budget (ex: $100/mois)
3. Vous recevrez un email si vous dépassez

---

## 🐛 Dépannage

### Erreur : "Could not load credentials"
```bash
# Vérifier que le fichier existe
dir c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json

# Vérifier la variable d'environnement
echo %GOOGLE_APPLICATION_CREDENTIALS%
```

### Erreur : "API not enabled"
- Retournez à l'étape 2 et vérifiez que les 3 APIs sont activées

### Erreur : "Permission denied"
- Vérifiez que les rôles sont bien attribués au compte de service (étape 3)

### Le pipeline ne bascule pas vers Google Cloud
```python
# Vérifier dans Django shell
python manage.py shell

>>> import os
>>> print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
>>> print(os.getenv('USE_GOOGLE_CLOUD'))
```

---

## ✅ Checklist finale

- [ ] Projet Google Cloud créé
- [ ] 3 APIs activées
- [ ] Compte de service créé avec les bons rôles
- [ ] Fichier JSON téléchargé et placé dans `/credentials/`
- [ ] `.env` créé avec `GOOGLE_APPLICATION_CREDENTIALS`
- [ ] `.gitignore` mis à jour
- [ ] Packages Python installés
- [ ] Test réussi
- [ ] `USE_GOOGLE_CLOUD=True` dans `.env`
- [ ] Serveur Django redémarré

---

## 🎉 Prêt !

Votre LinguaMeet utilise maintenant les **APIs professionnelles de Google Cloud** !

La qualité de traduction audio sera **nettement supérieure** :
- ✅ Transcription plus précise (95%+ de précision)
- ✅ Traduction plus naturelle
- ✅ Voix Neural2 ultra-réalistes
- ✅ Latence optimisée

**Profitez de votre système de traduction audio de qualité professionnelle !** 🚀🌍
