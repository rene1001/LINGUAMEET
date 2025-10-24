#!/usr/bin/env bash
set -euo pipefail

# Normaliser les fins de ligne si nécessaire
sed -i 's/\r$//' /app/entrypoint.sh || true

# Appliquer les migrations
python manage.py migrate --no-input

# Lancer Daphne (Render fournit $PORT)
PORT_TO_USE=${PORT:-8000}
echo "Starting Daphne on port ${PORT_TO_USE}..."
exec daphne -b 0.0.0.0 -p ${PORT_TO_USE} linguameet_project.asgi:application
