# 🌍 LinguaMeet - Conférences vocales multilingues en temps réel

**LinguaMeet** est une application web Django qui permet aux utilisateurs de participer à des conférences vocales multilingues en temps réel. Chaque participant parle dans sa langue et entend les autres dans sa langue préférée grâce à un pipeline AI complet : parole → transcription → traduction → synthèse vocale.

## 🚀 Fonctionnalités

- **Conférences en temps réel** avec WebSocket
- **Transcription automatique** avec Vosk
- **Traduction instantanée** avec Google Translate
- **Synthèse vocale** avec gTTS
- **Interface moderne** avec Bootstrap
- **Support de 10 langues** : Français, Anglais, Espagnol, Allemand, Italien, Portugais, Russe, Japonais, Coréen, Chinois
- **Gestion des participants** avec microphones ON/OFF
- **Responsive design** pour mobile et desktop

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │    │   WebSocket     │    │   Pipeline AI   │
│   Web (Bootstrap)│◄──►│   (Django       │◄──►│   (Vosk +       │
│                 │    │   Channels)     │    │   Google TTS)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Capture       │    │   Base de       │    │   Traitement    │
│   Audio         │    │   données       │    │   Audio         │
│   (WebRTC)      │    │   (SQLite)      │    │   (Async)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prérequis

- Python 3.8+
- pip
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)
- Microphone (pour participer aux conférences)

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd LINGUAMEET
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install django daphne channels redis vosk googletrans==4.0.0rc1 gtts numpy
```

### 5. Configurer la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 7. Démarrer le serveur

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : http://localhost:8000

## 🧪 Tests automatiques

Pour exécuter les tests automatiques :

```bash
python test_linguameet.py
```

Les tests vérifient :
- ✅ Modèles de base de données
- ✅ Support des langues
- ✅ Pipeline audio (transcription, traduction, synthèse)
- ✅ Connexion WebSocket

## 📖 Utilisation

### 1. Créer une réunion

1. Accédez à http://localhost:8000
2. Cliquez sur "Créer une réunion"
3. Entrez un nom pour la réunion
4. Choisissez la langue par défaut
5. Cliquez sur "Créer la réunion"

### 2. Rejoindre une réunion

1. Sur la page d'accueil, cliquez sur "Rejoindre une réunion"
2. Entrez le code UUID de la réunion
3. Configurez vos informations :
   - Votre nom
   - Langue de parole (celle dans laquelle vous parlez)
   - Langue de réception (celle dans laquelle vous voulez entendre)
4. Cliquez sur "Rejoindre la réunion"

### 3. Participer à la conférence

1. Autorisez l'accès au microphone
2. Utilisez le bouton microphone pour activer/désactiver votre micro
3. Parlez dans votre langue choisie
4. Écoutez les autres dans votre langue de réception

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Modèles Vosk (optionnel)

Pour une meilleure reconnaissance vocale, téléchargez les modèles Vosk :

```bash
# Créer le dossier pour les modèles
mkdir vosk_models

# Télécharger un modèle (exemple pour le français)
wget https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip
unzip vosk-model-small-fr-0.22.zip -d vosk_models/
```

## 📁 Structure du projet

```
LINGUAMEET/
├── linguameet_project/     # Configuration Django
│   ├── settings.py        # Paramètres
│   ├── urls.py           # URLs principales
│   ├── asgi.py          # Configuration ASGI
│   └── routing.py       # Routage WebSocket
├── conference/           # Application principale
│   ├── models.py        # Modèles Room et Participant
│   ├── views.py         # Vues Django
│   ├── consumers.py     # Consommateurs WebSocket
│   ├── ai_pipeline.py   # Pipeline AI
│   └── urls.py          # URLs de l'application
├── templates/           # Templates HTML
│   ├── base.html       # Template de base
│   └── conference/     # Templates de l'application
├── static/             # Fichiers statiques
│   ├── css/           # Styles CSS
│   └── js/            # JavaScript
├── test_linguameet.py  # Tests automatiques
├── manage.py          # Script Django
└── README.md          # Ce fichier
```

## 🛠️ Développement

### Ajouter une nouvelle langue

1. Modifiez `settings.py` :
```python
SUPPORTED_LANGUAGES = {
    # ... langues existantes ...
    'ar': 'العربية',  # Nouvelle langue
}
```

2. Mettez à jour `ai_pipeline.py` :
```python
self.vosk_language_map['ar'] = 'ar'
self.gtts_language_map['ar'] = 'ar'
```

### Personnaliser l'interface

- Modifiez `static/css/style.css` pour les styles
- Modifiez `templates/` pour l'interface HTML
- Modifiez `static/js/` pour le comportement JavaScript

## 🚀 Déploiement

### Production avec Gunicorn

```bash
pip install gunicorn
gunicorn linguameet_project.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
```

### Avec Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

1. Consultez la documentation
2. Vérifiez les issues existantes
3. Créez une nouvelle issue avec :
   - Description du problème
   - Étapes pour reproduire
   - Version de Python/Django
   - Logs d'erreur

## 🎯 Roadmap

- [ ] Support de plus de langues
- [ ] Interface d'administration
- [ ] Historique des conversations
- [ ] Partage d'écran
- [ ] Chat textuel
- [ ] Enregistrement des sessions
- [ ] API REST
- [ ] Application mobile

---

**✅ MVP LinguaMeet terminé avec succès !**

*Développé avec ❤️ pour faciliter les communications multilingues* # LinguaMeet
