# 🚀 Configuration Google Cloud - Guide Ultra-Rapide (15 min)

**Objectif : Passer de 50% à 100% !**

---

## ✅ Étape 1 : Créer un Projet (3 min)

### 1.1 Ouvrir Google Cloud Console
👉 **Lien direct** : https://console.cloud.google.com

### 1.2 Créer le projet
1. Cliquez sur **"Sélectionner un projet"** (en haut à gauche)
2. Cliquez sur **"Nouveau projet"**
3. Nom du projet : `linguameet-free`
4. Cliquez sur **"Créer"**
5. **Attendez** 10 secondes que le projet soit créé
6. Sélectionnez le projet créé

---

## ✅ Étape 2 : Activer les APIs (2 min)

### 2.1 Activer Speech-to-Text API
👉 **Lien direct** : https://console.cloud.google.com/apis/library/speech.googleapis.com

1. **Vérifiez** que votre projet `linguameet-free` est sélectionné (en haut)
2. Cliquez sur **"ACTIVER"**
3. Attendez quelques secondes

### 2.2 Activer Text-to-Speech API
👉 **Lien direct** : https://console.cloud.google.com/apis/library/texttospeech.googleapis.com

1. Cliquez sur **"ACTIVER"**
2. Attendez quelques secondes

✅ **Checkpoint** : Vous avez maintenant 2 APIs activées !

---

## ✅ Étape 3 : Créer un Compte de Service (5 min)

### 3.1 Accéder aux Comptes de Service
👉 **Lien direct** : https://console.cloud.google.com/iam-admin/serviceaccounts

### 3.2 Créer le compte
1. Cliquez sur **"CRÉER UN COMPTE DE SERVICE"** (en haut)

2. **Étape 1 - Détails du compte de service** :
   - Nom : `linguameet-service`
   - ID : `linguameet-service` (auto-généré)
   - Description : `Service pour LinguaMeet`
   - Cliquez sur **"CRÉER ET CONTINUER"**

3. **Étape 2 - Accorder des rôles** :
   - Cliquez sur **"Sélectionner un rôle"**
   - Dans la recherche, tapez : `Cloud Speech Client`
   - Sélectionnez : **"Cloud Speech Client"**
   - Cliquez sur **"+ AJOUTER UN AUTRE RÔLE"**
   - Tapez : `Cloud Text-to-Speech User`
   - Sélectionnez : **"Cloud Text-to-Speech User"**
   - Cliquez sur **"CONTINUER"**

4. **Étape 3 - Accorder l'accès aux utilisateurs** :
   - Laissez vide
   - Cliquez sur **"TERMINÉ"**

✅ **Checkpoint** : Votre compte de service est créé !

---

## ✅ Étape 4 : Télécharger la Clé JSON (3 min)

### 4.1 Créer une clé

1. Dans la liste des comptes de service, **cliquez** sur `linguameet-service@...`
2. Allez dans l'onglet **"CLÉS"** (en haut)
3. Cliquez sur **"AJOUTER UNE CLÉ"** → **"Créer une clé"**
4. Type de clé : **JSON** (sélectionné par défaut)
5. Cliquez sur **"CRÉER"**

📥 **Un fichier JSON est téléchargé automatiquement** (dans votre dossier Téléchargements)

Le nom du fichier ressemble à : `linguameet-free-1234567890ab.json`

---

## ✅ Étape 5 : Placer la Clé (2 min)

### 5.1 Déplacer le fichier

Ouvrez PowerShell ou CMD et exécutez :

```powershell
# Remplacez le nom du fichier par le vôtre !
move C:\Users\%USERNAME%\Downloads\linguameet-free-*.json c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
```

**OU** manuellement :
1. Ouvrez le dossier `Téléchargements`
2. Coupez le fichier JSON
3. Collez-le dans : `c:\wamp64\www\LangMeet\LINGUAMEET\credentials\`
4. Renommez-le en : `google-cloud-key.json`

### 5.2 Vérifier que le fichier existe

```powershell
dir c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
```

Vous devriez voir le fichier !

---

## ✅ Étape 6 : Activer dans .env (1 min)

### 6.1 Éditer le fichier .env

Ouvrez : `c:\wamp64\www\LangMeet\LINGUAMEET\.env`

### 6.2 Décommenter la ligne

**AVANT** :
```bash
# GOOGLE_APPLICATION_CREDENTIALS=c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
```

**APRÈS** (enlever le # au début) :
```bash
GOOGLE_APPLICATION_CREDENTIALS=c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
```

### 6.3 Sauvegarder le fichier

`Ctrl + S` ou File → Save

---

## ✅ Étape 7 : TESTER ! (1 min)

### 7.1 Lancer le test

```bash
cd c:\wamp64\www\LangMeet\LINGUAMEET
python test_config.py
```

### 7.2 Résultat attendu

Vous devriez voir :

```
============================================================
TEST DE CONFIGURATION LINGUAMEET
============================================================

1. Variables d'environnement:
------------------------------------------------------------
USE_FREE_PREMIUM: True
GEMINI_API_KEY: [OK] Definie
  -> AIzaSyAnnhrURu1ACdFF...
GOOGLE_APPLICATION_CREDENTIALS: [OK] Definie
  -> c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
  -> [OK] Fichier existe

2. Test Gemini API:
------------------------------------------------------------
Envoi d'une requete test a Gemini...
[OK] Gemini fonctionne !
Reponse : Hello

3. Test Google Cloud:
------------------------------------------------------------
Initialisation Speech-to-Text...
[OK] Google Speech-to-Text OK
Initialisation Text-to-Speech...
[OK] Google Text-to-Speech OK

4. Pipeline Audio:
------------------------------------------------------------
[OK] Pipeline GRATUIT Premium : ACTIF
   -> Google Speech-to-Text (transcription)
   -> Gemini AI (traduction)
   -> Google TTS (synthese vocale)

============================================================
RESUME
============================================================
[OK] Mode Free Premium active
[OK] Gemini API configure
[OK] Google Cloud configure

============================================================

TOUT EST CONFIGURE !
Lancez le serveur : python manage.py runserver
```

---

## 🎉 Étape 8 : LANCER LINGUAMEET !

```bash
python manage.py runserver
```

### Dans les logs, vous verrez :

```
🎓 Pipeline GRATUIT Premium activé (Google STT + Gemini + Google TTS)
✅ Google Speech-to-Text initialisé
✅ Gemini API initialisé (gemini-2.5-flash)
✅ Google Text-to-Speech initialisé
🎉 Pipeline GRATUIT Premium prêt !
```

### Ouvrez votre navigateur :

👉 http://localhost:8000

---

## 🐛 Problèmes Possibles

### Erreur : "could not find default credentials"

**Solution** : Vérifiez que :
1. Le fichier `google-cloud-key.json` existe bien dans `credentials/`
2. La ligne `GOOGLE_APPLICATION_CREDENTIALS` dans `.env` est décommentée (pas de # au début)
3. Le chemin est correct

### Erreur : "API not enabled"

**Solution** : Retournez à l'Étape 2 et vérifiez que les 2 APIs sont activées

### Erreur : "Permission denied"

**Solution** : Retournez à l'Étape 3.2 et vérifiez que les 2 rôles sont bien ajoutés :
- Cloud Speech Client
- Cloud Text-to-Speech User

---

## ✅ Checklist Finale

- [ ] Projet Google Cloud créé (`linguameet-free`)
- [ ] Speech-to-Text API activée
- [ ] Text-to-Speech API activée
- [ ] Compte de service créé (`linguameet-service`)
- [ ] 2 rôles ajoutés (Speech Client + TTS User)
- [ ] Clé JSON téléchargée
- [ ] Fichier placé dans `credentials/google-cloud-key.json`
- [ ] Ligne décommentée dans `.env`
- [ ] Test `python test_config.py` réussi
- [ ] Serveur lancé : `python manage.py runserver`

---

## 🎉 FÉLICITATIONS !

Vous avez maintenant **100%** de configuration !

**Votre LinguaMeet utilise :**
- ✅ Google Speech-to-Text (90-95% précision)
- ✅ Gemini AI 2.5 Flash (traduction intelligente)
- ✅ Google Text-to-Speech (voix naturelles)
- ✅ 100% GRATUIT avec quotas mensuels

**Profitez de votre système de traduction audio professionnel !** 🌍🚀

---

**Temps total : 15 minutes**
**Coût : 0€**
**Qualité : Professionnelle**
