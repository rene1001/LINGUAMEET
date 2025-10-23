# Guide Complet des Tests - LinguaMeet

## 📋 Vue d'Ensemble

Ce document décrit la suite complète de tests pour l'application LinguaMeet, couvrant **10 catégories de tests** pour garantir la qualité, la sécurité et la fiabilité de l'application.

---

## 🎯 Types de Tests Implémentés

### 1. ✅ Tests Fonctionnels (`test_functional.py`)
**Objectif** : Vérifier que toutes les fonctionnalités principales fonctionnent correctement

**Tests inclus** :
- Création et gestion des salles de conférence
- Création et gestion des participants
- Historique des conversations
- Navigation dans l'application
- Support des langues multiples
- Configuration WebSocket

**Commande** :
```bash
python manage.py test tests.test_functional
```

---

### 2. ⚡ Tests de Performance (`test_performance.py`)
**Objectif** : Mesurer les temps de réponse et l'optimisation de l'application

**Tests inclus** :
- Performance des requêtes de base de données
- Temps de chargement des pages
- Gestion des requêtes concurrentes
- Performance du pipeline audio
- Utilisation mémoire
- Taille des fichiers statiques

**Seuils acceptables** :
- Page d'accueil : < 1s
- Page de salle : < 1.5s
- Requêtes DB : < 0.5s
- Pipeline audio : < 5s (initialisation)

**Commande** :
```bash
python manage.py test tests.test_performance
```

---

### 3. 🔒 Tests de Sécurité (`test_security.py`)
**Objectif** : Détecter les vulnérabilités de sécurité

**Tests inclus** :
- Protection CSRF
- Injection SQL
- Attaques XSS
- Authentification et autorisation
- Validation des données
- Sécurité des uploads
- En-têtes HTTP sécurisés
- Protection des sessions
- Hachage des mots de passe
- Sécurité WebSocket

**Commande** :
```bash
python manage.py test tests.test_security
```

---

### 4. 🎨 Tests UI/UX (`test_ui_ux.py`)
**Objectif** : Vérifier l'expérience utilisateur et l'interface

**Tests inclus** :
- Design responsive
- Navigation intuitive
- Utilisabilité des formulaires
- Feedback visuel
- Éléments interactifs
- Parcours utilisateur complet
- Expérience mobile
- Performance UX

**Commande** :
```bash
python manage.py test tests.test_ui_ux
```

---

### 5. 🌐 Tests de Compatibilité (`test_compatibility.py`)
**Objectif** : Assurer la compatibilité multi-navigateurs et API

**Tests inclus** :
- Compatibilité navigateurs modernes
- API Media (getUserMedia)
- Support WebRTC
- Fonctionnalités JavaScript ES6+

**Navigateurs supportés** :
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

**Commande** :
```bash
python manage.py test tests.test_compatibility
```

---

### 6. 📈 Tests SEO (`test_seo.py`)
**Objectif** : Optimiser le référencement naturel

**Tests inclus** :
- Balises meta (title, description)
- Structure des titres (H1, H2, H3)
- URLs propres et lisibles
- Données structurées
- Sitemap (si applicable)

**Commande** :
```bash
python manage.py test tests.test_seo
```

---

### 7. ♿ Tests d'Accessibilité (`test_accessibility.py`)
**Objectif** : Conformité aux standards WCAG 2.1

**Tests inclus** :
- Attributs ARIA
- Navigation au clavier
- Support des lecteurs d'écran
- Attribut lang HTML
- Hiérarchie des titres
- Contraste des couleurs

**Standards** : WCAG 2.1 Level AA

**Commande** :
```bash
python manage.py test tests.test_accessibility
```

---

### 8. 🔌 Tests d'Intégration API (`test_api_integration.py`)
**Objectif** : Vérifier l'intégration avec les API externes

**Tests inclus** :
- Configuration Google Cloud API
- Gemini API
- WebSocket (Django Channels)
- Credentials et authentification

**APIs testées** :
- Google Speech-to-Text
- Gemini 2.5 Flash
- Google Text-to-Speech
- Django Channels Layer

**Commande** :
```bash
python manage.py test tests.test_api_integration
```

---

### 9. 🔄 Tests de Régression (`test_regression.py`)
**Objectif** : S'assurer qu'aucune fonctionnalité n'est cassée

**Tests inclus** :
- Fonctionnalités core inchangées
- URLs stables
- Modèles de données cohérents
- Compatibilité ascendante

**Commande** :
```bash
python manage.py test tests.test_regression
```

---

### 10. 📝 Tests de Contenu (`test_content.py`)
**Objectif** : Valider la qualité du contenu

**Tests inclus** :
- Présence du contenu principal
- Messages d'erreur clairs
- Support multilingue
- Cohérence du texte

**Commande** :
```bash
python manage.py test tests.test_content
```

---

## 🚀 Exécution des Tests

### Exécuter TOUS les tests avec rapport HTML

```bash
python run_all_tests.py
```

Cette commande :
- ✅ Exécute les 10 suites de tests
- ⏱️ Mesure les performances
- 📊 Génère un rapport HTML (`test_report.html`)
- 🎨 Affiche un résumé coloré dans le terminal

### Exécuter une suite spécifique

```bash
# Tests fonctionnels uniquement
python manage.py test tests.test_functional

# Tests de sécurité uniquement
python manage.py test tests.test_security

# Tests de performance uniquement
python manage.py test tests.test_performance
```

### Exécuter avec Django

```bash
# Tous les tests Django
python manage.py test tests

# Avec verbosité
python manage.py test tests --verbosity=2

# Un test spécifique
python manage.py test tests.test_functional.RoomFunctionalTests.test_create_room
```

---

## 📊 Interprétation des Résultats

### Code de Couleurs Terminal

- 🟢 **VERT** : Test réussi
- 🔴 **ROUGE** : Test échoué
- 🟡 **JAUNE** : Avertissement
- 🔵 **BLEU** : Information

### Rapport HTML

Le rapport `test_report.html` contient :
- **Résumé visuel** avec cartes statistiques
- **Tableau détaillé** de tous les tests
- **Durée d'exécution** de chaque suite
- **Statut** (PASS/FAIL) pour chaque catégorie
- **Recommandations** d'amélioration

### Métriques Importantes

| Métrique | Seuil Acceptable | Critique |
|----------|------------------|----------|
| Taux de réussite | > 95% | > 90% |
| Temps de réponse page | < 2s | < 3s |
| Temps DB query | < 500ms | < 1s |
| Couverture de code | > 80% | > 70% |

---

## 🛠️ Configuration des Tests

### Fichiers de Configuration

```
LINGUAMEET/
├── tests/
│   ├── __init__.py
│   ├── test_functional.py         # Tests fonctionnels
│   ├── test_performance.py        # Tests de performance
│   ├── test_security.py           # Tests de sécurité
│   ├── test_ui_ux.py              # Tests UI/UX
│   ├── test_compatibility.py      # Tests de compatibilité
│   ├── test_seo.py                # Tests SEO
│   ├── test_accessibility.py      # Tests d'accessibilité
│   ├── test_api_integration.py    # Tests d'intégration API
│   ├── test_regression.py         # Tests de régression
│   └── test_content.py            # Tests de contenu
├── run_all_tests.py               # Script master
└── test_report.html               # Rapport généré
```

### Variables d'Environnement pour Tests

Créer un fichier `.env.test` pour les tests :

```bash
DJANGO_SETTINGS_MODULE=linguameet_project.settings
USE_FREE_PREMIUM=True
GEMINI_API_KEY=your_test_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/test/credentials.json
```

---

## 🐛 Résolution des Problèmes

### Erreur : "No module named 'tests'"

```bash
# Assurez-vous que __init__.py existe dans tests/
touch tests/__init__.py
```

### Erreur : Base de données verrouillée

```bash
# Utiliser une base de test séparée
python manage.py test tests --settings=linguameet_project.test_settings
```

### Tests lents

```bash
# Exécuter en parallèle (Django 4.2+)
python manage.py test tests --parallel
```

### Échecs intermittents

- Vérifier les tests asynchrones
- Augmenter les timeouts
- Isoler les tests avec `@override_settings`

---

## 📈 Amélioration Continue

### Couverture de Code

```bash
# Installer coverage
pip install coverage

# Exécuter avec couverture
coverage run --source='.' manage.py test tests
coverage report
coverage html
```

### Tests de Charge

Pour des tests de charge avancés :

```bash
pip install locust
locust -f locustfile.py
```

### Tests E2E

Pour des tests end-to-end avec Selenium :

```bash
pip install selenium
python manage.py test tests.test_e2e
```

---

## ✅ Checklist de Tests Avant Production

- [ ] Tous les tests passent (100%)
- [ ] Couverture de code > 80%
- [ ] Aucune vulnérabilité de sécurité
- [ ] Performance acceptable (< 2s par page)
- [ ] Compatible multi-navigateurs
- [ ] Accessible (WCAG 2.1 AA)
- [ ] SEO optimisé
- [ ] Rapport HTML généré et vérifié
- [ ] Tests de régression OK
- [ ] Intégration API fonctionnelle

---

## 📚 Ressources

- **Django Testing** : https://docs.djangoproject.com/en/stable/topics/testing/
- **WCAG 2.1** : https://www.w3.org/WAI/WCAG21/quickref/
- **OWASP Top 10** : https://owasp.org/www-project-top-ten/
- **Web Performance** : https://web.dev/performance/

---

## 🎯 Objectifs de Qualité

| Catégorie | Objectif | Statut |
|-----------|----------|--------|
| Fonctionnalité | 100% des features testées | ✅ |
| Performance | < 2s par page | ✅ |
| Sécurité | 0 vulnérabilité critique | ✅ |
| Accessibilité | WCAG 2.1 AA | ✅ |
| SEO | Score > 90/100 | ✅ |
| Compatibilité | 4 navigateurs majeurs | ✅ |

---

**Dernière mise à jour** : 23 Octobre 2025
**Version** : 1.0.0
**Mainteneur** : Équipe LinguaMeet
