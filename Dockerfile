# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip --root-user-action=ignore && \
    pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copier le projet
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --no-input

# Rendre l'entrypoint exécutable
RUN chmod +x /app/entrypoint.sh || true

# Exposer un port par défaut (Render fournit $PORT au runtime)
EXPOSE 8000

# Utiliser un entrypoint pour appliquer les migrations puis lancer Daphne
ENTRYPOINT ["/app/entrypoint.sh"]
