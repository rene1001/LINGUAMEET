# 🚀 Migration vers le flux Google Meet

## Changements implémentés

### 1. **Modèle de langue unique** 
- Les participants utilisent maintenant **une seule langue** (parlent et écoutent dans la même langue)
- Ancien modèle : `langue_souhaitée` + `langue_parole` → Nouveau : `langue`

### 2. **Création instantanée de réunion**
- Cliquer sur "Nouvelle réunion" crée immédiatement la réunion (comme Google Meet)
- Redirection vers une page de partage avec le lien et le code

### 3. **Page de partage**
- Affichage du lien complet de la réunion
- Affichage du code UUID
- Boutons de copie pour partager facilement

### 4. **Accès par lien**
- Un utilisateur peut cliquer sur le lien partagé
- S'il n'est pas connecté : redirection vers login/inscription
- Après connexion : retour automatique vers la réunion

### 5. **Sélection de langue obligatoire**
- Avant d'entrer dans la réunion, l'utilisateur choisit sa langue
- Une seule langue : il parle ET écoute dans cette langue
- Interface claire avec drapeaux et explications

## Instructions d'installation

### Étape 1 : Appliquer les migrations de base de données

```powershell
# Se placer dans le dossier du projet
cd c:\wamp64\www\LangMeet\LINGUAMEET

# Activer l'environnement virtuel
.\venv\Scripts\activate

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### Étape 2 : Redémarrer le serveur

```powershell
# Arrêter le serveur si il tourne (Ctrl+C)
# Puis relancer
python manage.py runserver
```

### Étape 3 : Tester le nouveau flux

1. **Créer une réunion** :
   - Connexion à http://localhost:8000/
   - Cliquer sur "Nouvelle réunion"
   - → Redirection vers la page de partage

2. **Partager le lien** :
   - Copier le lien ou le code
   - Ouvrir dans un nouvel onglet (ou navigateur privé)

3. **Rejoindre avec le lien** :
   - Coller le lien
   - Si non connecté : créer un compte ou se connecter
   - → Redirection automatique vers la sélection de langue

4. **Choisir la langue** :
   - Sélectionner votre langue (ex: Français)
   - Cliquer sur "Rejoindre la réunion"
   - → Entrée dans la salle avec votre langue configurée

## Flux utilisateur complet

```
[Accueil] 
   ↓ Clic "Nouvelle réunion"
[Page de partage - Lien + Code]
   ↓ Copier et partager le lien
[Un autre utilisateur clique sur le lien]
   ↓ Si non connecté
[Login / Inscription]
   ↓ Après connexion
[Sélection de langue]
   ↓ Choix de la langue (une seule)
[Salle de conférence]
```

## Nouveaux fichiers créés

- `conference/templates/conference/room_ready.html` - Page de partage
- `conference/templates/conference/select_language.html` - Sélection de langue
- `conference/migrations/0002_merge_language_fields.py` - Migration DB

## Fichiers modifiés

- `conference/models.py` - Modèle Participant avec langue unique
- `conference/views_auth.py` - Nouvelles vues pour le flux
- `conference/views.py` - Mise à jour pour la langue unique
- `conference/urls.py` - Nouvelles routes
- `conference/templates/conference/home_meet.html` - Création instantanée

## Notes importantes

⚠️ **Migration de données** : 
La migration conserve la valeur de `langue_parole` comme nouvelle valeur de `langue` pour les participants existants.

✅ **Compatibilité** :
Les anciennes URLs restent fonctionnelles pour la compatibilité.

🌍 **Traduction automatique** :
- Si vous parlez en Français et un autre participant est en Anglais
- Vous entendrez l'autre en Français (traduit automatiquement)
- L'autre vous entendra en Anglais (traduit automatiquement)
