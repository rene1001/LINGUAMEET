#!/usr/bin/env bash
# Script de build pour Render.com

set -o errexit  # Arrêter si une commande échoue

echo "🔧 Normalisation des fins de ligne (CRLF -> LF)..."
# Convertir les finales de ligne Windows si présentes, pour éviter $'\r' errors
sed -i 's/\r$//' build.sh || true
sed -i 's/\r$//' start.sh || true

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗂️ Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🗄️ Migration de la base de données..."
python manage.py migrate --no-input

echo "✅ Build terminé avec succès !"
