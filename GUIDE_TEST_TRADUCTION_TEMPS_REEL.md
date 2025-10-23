# Guide de Test - Traduction en Temps Réel LinguaMeet

## ✅ Tests Automatisés Réussis (100%)

Tous les tests automatisés ont été exécutés avec succès :
- ✅ Configuration de l'environnement (.env)
- ✅ Modèles de base de données
- ✅ Pipeline audio de traduction (Google + Gemini)
- ✅ Configuration WebSocket (Django Channels)
- ✅ Fichiers statiques JavaScript

**Taux de réussite : 100%**

---

## 🎯 Tests Manuels - Instructions

### 1. Démarrer le Serveur

```bash
cd c:\wamp64\www\LangMeet\LINGUAMEET
python manage.py runserver
```

Le serveur démarrera sur : **http://localhost:8000**

---

### 2. Test Basique - Un Seul Utilisateur

#### Étape 1 : Créer une Salle
1. Ouvrez votre navigateur : http://localhost:8000
2. Cliquez sur **"Créer une nouvelle réunion"**
3. Donnez un nom à votre salle (ex: "Test Traduction")
4. Sélectionnez la langue par défaut : **Français**
5. Cliquez sur **"Créer"**

#### Étape 2 : Rejoindre la Salle
1. Entrez votre nom (ex: "Testeur")
2. **Langue que vous parlez** : Français
3. **Langue que vous souhaitez recevoir** : Anglais
4. Cliquez sur **"Rejoindre la réunion"**

#### Étape 3 : Autoriser le Microphone
1. Le navigateur va demander l'accès au microphone
2. Cliquez sur **"Autoriser"**

#### Étape 4 : Tester la Traduction
1. Assurez-vous que le bouton microphone est VERT (actif)
2. Parlez en français dans votre microphone
3. Vérifiez :
   - ✅ La transcription s'affiche en temps réel en bas de l'écran
   - ✅ Le texte original en français apparaît
   - ✅ La traduction en anglais s'affiche
   - ✅ L'audio traduit est joué automatiquement

**Exemples de phrases à tester :**
- "Bonjour, comment allez-vous ?"
- "Je suis très content d'utiliser cette application"
- "La météo est magnifique aujourd'hui"

---

### 3. Test Avancé - Plusieurs Utilisateurs

#### Configuration Requise
- 2 ordinateurs différents OU
- 2 navigateurs différents (Chrome + Firefox) OU
- 1 navigateur normal + 1 fenêtre de navigation privée

#### Scénario de Test

**Utilisateur 1 (Français → Anglais)**
1. Créer une salle de réunion
2. Nom : "Alice"
3. Parle : Français
4. Reçoit : Anglais
5. Copier l'URL de la salle

**Utilisateur 2 (Anglais → Français)**
1. Ouvrir l'URL copiée
2. Nom : "Bob"
3. Parle : Anglais
4. Reçoit : Français
5. Rejoindre la réunion

#### Tests à Effectuer

**Test 1 : Alice parle en français**
- Alice dit : "Bonjour Bob, comment vas-tu ?"
- Bob devrait entendre en anglais : "Hello Bob, how are you?"
- Vérifier la transcription en temps réel

**Test 2 : Bob répond en anglais**
- Bob dit : "I'm fine, thank you! And you?"
- Alice devrait entendre en français : "Je vais bien, merci ! Et toi ?"
- Vérifier la transcription en temps réel

**Test 3 : Conversation naturelle**
- Discutez normalement pendant 2-3 minutes
- Changez de sujets
- Vérifiez que la traduction reste fluide

---

### 4. Tests de Qualité Audio

#### Test du Microphone
- Parlez à distance normale (~30cm)
- Évitez le bruit de fond
- Parlez clairement mais naturellement

#### Test des Langues Supportées
Testez différentes combinaisons :

| Langue Source | Langue Cible | Test |
|---------------|--------------|------|
| Français      | Anglais      | ✅   |
| Anglais       | Français     | ✅   |
| Français      | Espagnol     | ✅   |
| Anglais       | Allemand     | ✅   |
| Espagnol      | Italien      | ✅   |

#### Phrases de Test par Langue

**Français :**
- "Bonjour, je m'appelle [nom]. Enchanté de vous rencontrer."
- "Quel temps fait-il chez vous aujourd'hui ?"

**Anglais :**
- "Hello, my name is [name]. Nice to meet you."
- "What's the weather like where you are today?"

**Espagnol :**
- "Hola, me llamo [nombre]. Encantado de conocerte."
- "¿Qué tiempo hace donde estás hoy?"

---

### 5. Tests de Performance

#### Test de Latence
1. Chronométrer le temps entre :
   - Fin de votre phrase → Début de l'audio traduit
2. **Latence acceptable** : 2-4 secondes
3. Si > 5 secondes : vérifier la connexion internet

#### Test de Qualité
1. **Transcription** :
   - ✅ Texte correct à 90%+
   - ✅ Ponctuation appropriée
   
2. **Traduction** :
   - ✅ Sens préservé
   - ✅ Naturel dans la langue cible
   
3. **Synthèse vocale** :
   - ✅ Prononciation claire
   - ✅ Intonation naturelle

---

### 6. Tests de Stabilité

#### Test de Connexion
1. Rejoindre une salle
2. Attendre 5 minutes sans parler
3. Parler à nouveau
4. ✅ La connexion doit rester active

#### Test de Reconnexion
1. Couper le WiFi pendant 10 secondes
2. Rallumer le WiFi
3. ✅ Le système doit se reconnecter automatiquement

#### Test de Plusieurs Participants
1. Ajouter 3-4 participants dans la même salle
2. Tout le monde parle à tour de rôle
3. ✅ Toutes les traductions doivent fonctionner

---

### 7. Vérification des Fonctionnalités

#### Contrôles Audio/Vidéo
- [ ] Bouton microphone ON/OFF fonctionne
- [ ] Indicateur visuel du microphone actif
- [ ] Barre de visualisation audio s'anime

#### Transcription en Temps Réel
- [ ] Zone de transcription visible en bas
- [ ] Texte original affiché
- [ ] Texte traduit affiché
- [ ] Mise à jour en temps réel

#### Interface Utilisateur
- [ ] Liste des participants visible
- [ ] Langues des participants affichées
- [ ] Statut de connexion affiché
- [ ] Messages système clairs

---

### 8. Historique des Conversations

1. Après une conversation, cliquer sur **"Historique"**
2. Vérifier que les conversations sont sauvegardées
3. Vérifier les informations :
   - ✅ Texte original
   - ✅ Texte traduit
   - ✅ Langues source/cible
   - ✅ Horodatage
   - ✅ Fichiers audio téléchargeables

---

## 🐛 Résolution de Problèmes

### Le microphone ne fonctionne pas
1. Vérifier les permissions du navigateur
2. Tester le microphone : chrome://settings/content/microphone
3. Utiliser Chrome ou Firefox (recommandé)

### Pas de traduction
1. Vérifier le fichier `.env` :
   - GEMINI_API_KEY configuré
   - GOOGLE_APPLICATION_CREDENTIALS configuré
2. Vérifier les logs du serveur
3. Relancer le serveur : `python manage.py runserver`

### Mauvaise qualité audio
1. Parler plus clairement
2. Réduire le bruit de fond
3. Rapprocher le microphone
4. Vérifier la connexion internet

### Latence élevée
1. Vérifier la connexion internet (min 1 Mbps)
2. Fermer les applications gourmandes
3. Utiliser une connexion filaire si possible

---

## 📊 Métriques de Qualité

### Objectifs de Performance
- **Transcription** : >90% de précision
- **Traduction** : Sens préservé, naturel
- **Latence** : <4 secondes
- **Uptime** : >95% de stabilité

### Rapport de Bug
Si vous trouvez un problème :
1. Notez les étapes pour le reproduire
2. Copiez les messages d'erreur
3. Vérifiez la console du navigateur (F12)
4. Vérifiez les logs du serveur Django

---

## 🎓 Configuration du Pipeline

Votre système utilise actuellement :

**Pipeline : Google + Gemini (Gratuit Premium)**
- 🎤 **STT** : Google Speech-to-Text (60 min/mois)
- 🌍 **Traduction** : Gemini 2.5 Flash (60 req/min)
- 🔊 **TTS** : Google Text-to-Speech (1M chars/mois)

### Quotas Disponibles
- Speech-to-Text : 60 minutes/mois
- Gemini API : 60 requêtes/minute (illimité mensuel)
- Text-to-Speech : 1 million de caractères/mois

**Ces quotas sont GRATUITS et suffisants pour vos tests !**

---

## ✅ Checklist Finale

Avant de considérer les tests terminés :

- [ ] Serveur démarre sans erreur
- [ ] Page d'accueil accessible
- [ ] Création de salle fonctionne
- [ ] Rejoindre une salle fonctionne
- [ ] Permission microphone accordée
- [ ] Transcription en temps réel fonctionne
- [ ] Traduction correcte
- [ ] Audio traduit joué correctement
- [ ] Plusieurs utilisateurs peuvent se parler
- [ ] Historique sauvegardé
- [ ] Aucun message d'erreur dans la console

---

## 📝 Notes Importantes

1. **Premier lancement** : La première traduction peut prendre 5-10 secondes (chargement des modèles)
2. **Quotas** : Surveillez vos quotas Google Cloud sur la console
3. **Langues** : 10 langues supportées (fr, en, es, de, it, pt, ru, ja, ko, zh)
4. **Navigateurs** : Chrome et Firefox recommandés
5. **HTTPS** : Pour la production, utilisez HTTPS (requis pour le microphone)

---

## 🚀 Prochaines Étapes

Une fois les tests réussis :
1. Tester avec des utilisateurs réels
2. Mesurer la satisfaction utilisateur
3. Collecter des retours sur la qualité
4. Optimiser selon les besoins
5. Préparer le déploiement en production

---

## 📞 Support

Consultez les guides de documentation :
- `README.md` - Vue d'ensemble
- `DEMARRAGE_RAPIDE.md` - Guide de démarrage
- `SETUP_FREE_PREMIUM.md` - Configuration du pipeline gratuit
- `GUIDE_ETUDIANT.md` - Guide pour étudiants

**Bon test ! 🎉**
