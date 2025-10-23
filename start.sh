#!/usr/bin/env bash
# Script de démarrage pour Render.com

set -o errexit  # Arrêter si une commande échoue

echo "🚀 Démarrage de LinguaMeet avec Daphne..."

# Démarrer Daphne (serveur ASGI pour Django Channels et WebSockets)
# Port automatiquement fourni par Render via $PORT
exec daphne -b 0.0.0.0 -p $PORT linguameet_project.asgi:application
