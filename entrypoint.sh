#!/usr/bin/env bash
set -euo pipefail

# Normaliser les fins de ligne si nécessaire
sed -i 's/\r$//' /app/entrypoint.sh || true

retry() {
  local max_attempts=$1; shift
  local delay=$1; shift
  local attempt=1
  until "$@"; do
    if (( attempt >= max_attempts )); then
      echo "Command failed after ${attempt} attempts: $*"
      return 1
    fi
    echo "Attempt ${attempt} failed. Retrying in ${delay}s..."
    attempt=$(( attempt + 1 ))
    sleep "${delay}"
  done
}

echo "Applying migrations..."
retry 5 5 python manage.py migrate --no-input

echo "Collecting static files..."
retry 3 5 python manage.py collectstatic --no-input

# Lancer Daphne (Render fournit $PORT)
PORT_TO_USE=${PORT:-8000}
echo "Starting Daphne on port ${PORT_TO_USE}..."
exec daphne -b 0.0.0.0 -p ${PORT_TO_USE} linguameet_project.asgi:application
