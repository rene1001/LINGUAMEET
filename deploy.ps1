# =============================================================================
# Script de Déploiement LinguaMeet sur Google Cloud Run
# =============================================================================
# Usage: .\deploy.ps1
# =============================================================================

param(
    [string]$ProjectId = "gen-lang-client-0170871086",
    [string]$Region = "europe-west1",
    [string]$ServiceName = "linguameet",
    [switch]$SkipBuild,
    [switch]$SetupOnly
)

# Couleurs pour les messages
function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host "ℹ $msg" -ForegroundColor Cyan }
function Write-Warning { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }

Write-Host "================================" -ForegroundColor Magenta
Write-Host "  LinguaMeet - Cloud Deployment" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta
Write-Host ""

# Vérifier que gcloud est installé
Write-Info "Vérification de Google Cloud SDK..."
try {
    $gcloudVersion = gcloud version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Google Cloud SDK détecté"
    } else {
        throw "gcloud non trouvé"
    }
} catch {
    Write-Error "Google Cloud SDK n'est pas installé"
    Write-Info "Installez-le depuis: https://cloud.google.com/sdk/docs/install"
    exit 1
}

# Configuration du projet
Write-Info "Configuration du projet Google Cloud..."
gcloud config set project $ProjectId
gcloud config set run/region $Region

# Vérifier l'authentification
Write-Info "Vérification de l'authentification..."
$currentAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
if ($currentAccount) {
    Write-Success "Connecté en tant que: $currentAccount"
} else {
    Write-Warning "Non authentifié. Lancement de l'authentification..."
    gcloud auth login
}

# Activer les APIs nécessaires
Write-Info "Activation des APIs Google Cloud..."
$apis = @(
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com"
)

foreach ($api in $apis) {
    Write-Info "  - $api"
    gcloud services enable $api --quiet 2>$null
}
Write-Success "APIs activées"

if ($SetupOnly) {
    Write-Success "Configuration initiale terminée !"
    Write-Info "Vous pouvez maintenant déployer avec: .\deploy.ps1"
    exit 0
}

# Vérifier que les variables d'environnement sont définies
Write-Info "Vérification des variables d'environnement..."

$secretKey = Read-Host "Entrez votre SECRET_KEY Django (ou appuyez sur Entrée pour générer)"
if ([string]::IsNullOrWhiteSpace($secretKey)) {
    Write-Info "Génération d'une nouvelle SECRET_KEY..."
    $secretKey = -join ((65..90) + (97..122) + (48..57) + @(33, 64, 35, 36, 37, 94, 38, 42) | Get-Random -Count 50 | % {[char]$_})
    Write-Success "SECRET_KEY générée"
}

# Déploiement
Write-Info "Déploiement de l'application sur Cloud Run..."
Write-Host ""

if ($SkipBuild) {
    Write-Warning "Mode SkipBuild: utilisation de l'image existante"
    gcloud run deploy $ServiceName `
        --platform managed `
        --region $Region `
        --allow-unauthenticated `
        --memory 1Gi `
        --timeout 3600 `
        --max-instances 10 `
        --set-env-vars "DEBUG=False,SECRET_KEY=$secretKey"
} else {
    Write-Info "Construction et déploiement de l'image Docker..."
    gcloud run deploy $ServiceName `
        --source . `
        --platform managed `
        --region $Region `
        --allow-unauthenticated `
        --memory 1Gi `
        --timeout 3600 `
        --max-instances 10 `
        --set-env-vars "DEBUG=False,SECRET_KEY=$secretKey"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Success "Déploiement réussi !"
    
    # Récupérer l'URL du service
    Write-Info "Récupération de l'URL du service..."
    $serviceUrl = gcloud run services describe $ServiceName --region $Region --format="value(status.url)"
    
    if ($serviceUrl) {
        Write-Host ""
        Write-Host "================================" -ForegroundColor Green
        Write-Host "  Application déployée avec succès !" -ForegroundColor Green
        Write-Host "================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "URL de l'application: " -NoNewline
        Write-Host $serviceUrl -ForegroundColor Yellow
        Write-Host ""
        
        # Mettre à jour ALLOWED_HOSTS et CSRF_TRUSTED_ORIGINS
        Write-Info "Mise à jour des paramètres de sécurité..."
        $hostname = $serviceUrl -replace "https://", ""
        
        gcloud run services update $ServiceName `
            --region $Region `
            --update-env-vars "ALLOWED_HOSTS=$hostname,.run.app" `
            --update-env-vars "CSRF_TRUSTED_ORIGINS=$serviceUrl" `
            --quiet
        
        Write-Success "Paramètres de sécurité mis à jour"
        
        # Proposer d'ouvrir dans le navigateur
        $openBrowser = Read-Host "Voulez-vous ouvrir l'application dans le navigateur ? (O/N)"
        if ($openBrowser -eq "O" -or $openBrowser -eq "o") {
            Start-Process $serviceUrl
        }
        
        Write-Host ""
        Write-Info "Commandes utiles:"
        Write-Host "  - Voir les logs: " -NoNewline
        Write-Host "gcloud run services logs tail $ServiceName --region $Region" -ForegroundColor Cyan
        Write-Host "  - Mettre à jour: " -NoNewline
        Write-Host ".\deploy.ps1" -ForegroundColor Cyan
        Write-Host ""
        
    } else {
        Write-Warning "Impossible de récupérer l'URL du service"
    }
} else {
    Write-Error "Échec du déploiement"
    Write-Info "Consultez les logs pour plus d'informations:"
    Write-Host "  gcloud builds list --limit 5" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Success "Terminé !"
