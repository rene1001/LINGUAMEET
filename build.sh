#!/usr/bin/env bash
# Script de build pour Render.com

set -o errexit  # Arrêter si une commande échoue

echo "🔧 Normalisation des fins de ligne (CRLF -> LF)..."
# Convertir les finales de ligne Windows si présentes, pour éviter $'\r' errors
sed -i 's/\r$//' build.sh 2>/dev/null || true
sed -i 's/\r$//' start.sh 2>/dev/null || true

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔐 Configuration des credentials Google Cloud..."
# Si GOOGLE_APPLICATION_CREDENTIALS_JSON est définie, créer le fichier de credentials
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS_JSON" ]; then
    echo "Création du fichier credentials depuis variable d'environnement..."
    mkdir -p /opt/render/project/src/credentials
    echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" | base64 -d > /opt/render/project/src/credentials/google-cloud-key.json
    export GOOGLE_APPLICATION_CREDENTIALS=/opt/render/project/src/credentials/google-cloud-key.json
    echo "✅ Credentials Google Cloud configurées"
else
    echo "⚠️  GOOGLE_APPLICATION_CREDENTIALS_JSON non définie - Le système de traduction ne fonctionnera pas"
fi

echo "🗂️ Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🗄️ Migration de la base de données..."
python manage.py migrate --no-input

echo "👤 Création du superutilisateur admin..."
python create_admin.py || echo "⚠️  Erreur lors de la création de l'admin (peut-être existe déjà)"

echo "✅ Build terminé avec succès !"
