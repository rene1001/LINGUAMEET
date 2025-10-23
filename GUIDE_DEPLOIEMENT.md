# Guide de Déploiement - LinguaMeet

**Version** : 1.0.0  
**Date** : 23 Octobre 2025

---

## 🎯 Pré-requis

### Serveur
- Python 3.8+
- PostgreSQL 12+ ou SQLite
- Redis 6.0+ (production)
- Nginx
- SSL/TLS (Let's Encrypt)

### Services
- Google Cloud (Speech-to-Text, Text-to-Speech)
- Gemini API

---

## 📋 Checklist Pré-Déploiement

- [ ] DEBUG = False
- [ ] SECRET_KEY sécurisée
- [ ] ALLOWED_HOSTS configuré
- [ ] Variables .env
- [ ] Migrations appliquées
- [ ] collectstatic exécuté
- [ ] HTTPS configuré

---

## 🚀 Étapes Rapides

### 1. Installer dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration .env
```env
SECRET_KEY=votre_cle_secrete
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=postgresql://user:pass@localhost/linguameet_db
```

### 3. Migrations
```bash
python manage.py migrate
python manage.py collectstatic
```

### 4. Lancer avec Gunicorn
```bash
gunicorn linguameet_project.asgi:application -k uvicorn.workers.UvicornWorker
```

Voir documentation complète dans le README.
