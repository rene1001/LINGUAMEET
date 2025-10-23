# 🎓 Configuration GRATUITE Premium pour Étudiants

## 🌟 Solution Idéale pour Étudiants

Cette configuration utilise les **quotas GRATUITS** des APIs professionnelles :

| API | Quota GRATUIT | Valeur |
|-----|---------------|--------|
| **Google Speech-to-Text** | 60 minutes/mois | Transcription précise |
| **Gemini API** | 60 requêtes/minute | Traduction intelligente |
| **Google Text-to-Speech** | 1M caractères/mois | Voix naturelles |

**COÛT TOTAL : 0€ !** 🎉

---

## ✅ Étape 1 : Obtenir la clé Gemini API (2 minutes)

### C'est 100% GRATUIT !

1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Connectez-vous avec votre compte Google

3. Cliquez sur **"Create API Key"**

4. Copiez la clé : `AIza...`

**C'est tout !** Gemini est gratuit pour toujours (60 req/min) 🎉

---

## ✅ Étape 2 : Configuration Google Cloud (15 minutes)

### Pour Speech-to-Text et Text-to-Speech GRATUITS

1. **Créer un projet Google Cloud**
   - Allez sur [Google Cloud Console](https://console.cloud.google.com)
   - Cliquez **"Créer un projet"**
   - Nom : `linguameet-free`
   - Pas besoin de carte bancaire pour les quotas gratuits ! 💳❌

2. **Activer les 2 APIs**
   
   a. **Cloud Speech-to-Text API**
   - [Lien direct](https://console.cloud.google.com/apis/library/speech.googleapis.com)
   - Cliquez **"Activer"**
   - ✅ 60 minutes/mois GRATUIT
   
   b. **Cloud Text-to-Speech API**
   - [Lien direct](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
   - Cliquez **"Activer"**
   - ✅ 1M caractères/mois GRATUIT (Standard voices)

3. **Créer une clé de service**
   - **"IAM et administration"** → **"Comptes de service"**
   - **"Créer un compte de service"**
   - Nom : `linguameet-free`
   - Rôles à ajouter :
     - `Cloud Speech Client`
     - `Cloud Text-to-Speech User`
   - **"Créer une clé"** → **JSON**
   - Le fichier est téléchargé 📥

---

## ✅ Étape 3 : Configuration dans le Projet (5 minutes)

### 1. Créer le dossier credentials

```bash
# Créer le dossier
mkdir c:\wamp64\www\LangMeet\LINGUAMEET\credentials

# Déplacer le fichier JSON téléchargé
move Downloads\linguameet-free-*.json c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
```

### 2. Créer le fichier .env

Créez `c:\wamp64\www\LangMeet\LINGUAMEET\.env` :

```bash
# APIs GRATUITES pour étudiants 🎓

# Gemini API (GRATUIT - 60 req/min)
GEMINI_API_KEY=AIza_votre_clé_ici

# Google Cloud credentials (GRATUIT - 60 min STT + 1M chars TTS/mois)
GOOGLE_APPLICATION_CREDENTIALS=c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json

# Activer le pipeline gratuit premium
USE_FREE_PREMIUM=True
```

### 3. Sécurité : Mettre à jour .gitignore

Ajoutez dans `.gitignore` :
```
# Credentials (ne JAMAIS commiter)
credentials/
.env
*.json
```

---

## ✅ Étape 4 : Installer les Dépendances

```bash
# Activer l'environnement virtuel
cd c:\wamp64\www\LangMeet\LINGUAMEET
.\venv\Scripts\activate

# Installer les packages (GRATUITS)
pip install google-cloud-speech
pip install google-cloud-texttospeech
pip install google-generativeai
pip install python-dotenv
```

---

## ✅ Étape 5 : Tester l'Installation

```bash
# Test rapide
python -c "
import asyncio
import sys
import os
sys.path.append('.')

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

from conference.ai_pipeline_free_premium import FreePremiumAudioProcessor

async def test():
    processor = FreePremiumAudioProcessor()
    if processor.is_ready:
        print('✅ Pipeline GRATUIT Premium configuré!')
        print('   - Google Speech-to-Text: OK')
        print('   - Gemini API: OK')
        print('   - Google TTS: OK')
        await processor.test_pipeline()
    else:
        print('❌ Problème de configuration')
        print('Vérifiez .env et credentials/')

asyncio.run(test())
"
```

Si vous voyez `✅ Pipeline GRATUIT Premium configuré!`, c'est bon ! 🎉

---

## 🔄 Activer dans LinguaMeet

Modifiez `conference/consumers.py` :

```python
# Au début du fichier, après les imports
import os
from dotenv import load_dotenv
load_dotenv()

# Remplacez la ligne d'import de AudioProcessor par :
USE_FREE_PREMIUM = os.getenv('USE_FREE_PREMIUM', 'False').lower() == 'true'

if USE_FREE_PREMIUM:
    try:
        from .ai_pipeline_free_premium import FreePremiumAudioProcessor as AudioProcessor
        logger.info("🎓 Pipeline GRATUIT Premium activé (étudiant)")
    except ImportError:
        from .ai_pipeline import AudioProcessor
        logger.warning("⚠️ Fallback vers pipeline standard")
else:
    from .ai_pipeline import AudioProcessor
```

**OU** plus simple, je peux le faire pour vous ! 😊

---

## 📊 Quotas Gratuits en Détail

### Ce que vous obtenez GRATUITEMENT chaque mois :

#### 1. Google Speech-to-Text
- **60 minutes** de transcription
- Équivaut à environ **120 conversations** de 30 secondes
- Qualité : 90-95% de précision
- ✅ Largement suffisant pour tester et développer !

#### 2. Gemini API
- **60 requêtes par minute**
- **1500 requêtes par jour**
- Équivaut à **1500 traductions par jour**
- ✅ Illimité pour vos besoins !

#### 3. Google Text-to-Speech (Standard)
- **1 million de caractères**
- Équivaut à environ **5000 réponses audio**
- Voix Standard (bonne qualité, pas Neural2)
- ✅ Plus que suffisant !

### Estimation d'utilisation réaliste

Pour **100 conversations de 2 minutes chacune** :
- STT : 200 minutes → ❌ Dépasserait le quota
- Gemini : 100 traductions → ✅ OK (1500/jour)
- TTS : ~50,000 caractères → ✅ OK (1M/mois)

**Solution** : Les 60 minutes STT suffisent pour ~30 conversations de 2 minutes, parfait pour développer et tester !

---

## 🎯 Avantages de Cette Solution

| Avantage | Détail |
|----------|--------|
| **💰 Coût** | 0€ - Totalement gratuit |
| **📈 Qualité** | Transcription : 90-95%<br>Traduction : Gemini AI<br>Voix : Standard (bonnes) |
| **🚀 Performance** | APIs cloud optimisées |
| **📚 Apprentissage** | APIs professionnelles réelles |
| **🔄 Évolutivité** | Facile de passer au payant plus tard |

---

## 🆚 Comparaison avec Vosk/gTTS

| | Vosk/gTTS (Ancien) | Free Premium (Nouveau) |
|---|---|---|
| **Transcription** | 70-80% | 90-95% |
| **Traduction** | googletrans (instable) | Gemini (stable) |
| **Voix** | Robotique | Naturelle (Standard) |
| **Fiabilité** | Moyenne | Excellente |
| **Coût** | 0€ | 0€ |

**Même prix, MEILLEURE qualité !** 🎉

---

## ⚠️ Limitations du Quota Gratuit

### Que se passe-t-il si vous dépassez ?

1. **Speech-to-Text** (60 min/mois)
   - Après 60 min : Facturation activée OU erreur
   - Solution : Monitorer l'utilisation

2. **Gemini** (60 req/min, 1500/jour)
   - Après quota : Erreur 429 (rate limit)
   - Solution : Largement suffisant normalement

3. **TTS** (1M chars/mois)
   - Après 1M : Facturation activée OU erreur
   - Solution : Largement suffisant

### Comment éviter les dépassements ?

1. **Ne pas activer la facturation** sur Google Cloud
   - Comme ça, impossible de dépasser (juste erreur)

2. **Monitorer dans Google Cloud Console**
   - Voir l'utilisation en temps réel
   - [Dashboard](https://console.cloud.google.com)

3. **Configurer des alertes** (optionnel)
   - Email quand 80% du quota utilisé

---

## 🐛 Dépannage

### Erreur : "Gemini API key not found"
```bash
# Vérifier la clé dans .env
cat .env | grep GEMINI

# Ou sous Windows
type .env | findstr GEMINI
```

### Erreur : "Google credentials not found"
```bash
# Vérifier le fichier
dir c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json

# Vérifier la variable
echo %GOOGLE_APPLICATION_CREDENTIALS%
```

### Pipeline ne bascule pas
```python
# Dans Django shell
python manage.py shell

>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> print(os.getenv('USE_FREE_PREMIUM'))
>>> print(os.getenv('GEMINI_API_KEY'))
>>> print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
```

---

## ✅ Checklist Finale

- [ ] Compte Google créé
- [ ] Clé Gemini API obtenue (`AIza...`)
- [ ] Projet Google Cloud créé
- [ ] 2 APIs activées (Speech-to-Text, Text-to-Speech)
- [ ] Compte de service créé
- [ ] Fichier JSON téléchargé
- [ ] Dossier `/credentials/` créé
- [ ] Fichier JSON placé dans `/credentials/`
- [ ] Fichier `.env` créé avec les 3 variables
- [ ] `.gitignore` mis à jour
- [ ] Packages Python installés
- [ ] Test réussi
- [ ] Serveur Django redémarré

---

## 🎉 Félicitations !

Votre LinguaMeet utilise maintenant des **APIs professionnelles GRATUITES** !

### Ce qui a changé :

✅ **Transcription** : 70% → **90-95%** de précision
✅ **Traduction** : googletrans → **Gemini AI** (stable et intelligent)
✅ **Voix** : Robotique → **Naturelle** (Google Standard)
✅ **Fiabilité** : Instable → **Professionnelle**
✅ **Coût** : 0€ → **0€** (inchangé !)

### Quand vous aurez de l'argent :

Vous pourrez facilement upgrader vers :
- **Neural2 voices** (encore plus naturelles) : +$16/1M chars
- **Enhanced STT** (99% précision) : +quelques $ par heure
- Plus de quota

Mais pour l'instant, **profitez de la qualité professionnelle GRATUITE** ! 🚀🎓

---

## 💡 Conseil Pro

**Testez d'abord avec quelques conversations** pour voir la différence de qualité.

Vous allez remarquer :
- Transcription beaucoup plus précise
- Traduction plus naturelle avec Gemini
- Voix plus agréable à écouter

**Bonne chance avec votre projet étudiant !** 🎓🌍

---

## 📚 Ressources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Cloud Free Tier](https://cloud.google.com/free)
- [Speech-to-Text Pricing](https://cloud.google.com/speech-to-text/pricing)
- [Text-to-Speech Pricing](https://cloud.google.com/text-to-speech/pricing)
