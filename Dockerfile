# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port 8080 (requis par Cloud Run)
EXPOSE 8080

# Lancer le serveur avec Daphne (ASGI server pour Django Channels)
CMD exec daphne -b 0.0.0.0 -p 8080 linguameet_project.asgi:application
