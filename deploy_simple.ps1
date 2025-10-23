# =============================================================================
# Script de Déploiement LinguaMeet sur Google Cloud Run - Version Simple
# =============================================================================

$ProjectId = "gen-lang-client-0170871086"
$Region = "europe-west1"
$ServiceName = "linguameet"

Write-Host ""
Write-Host "================================" -ForegroundColor Magenta
Write-Host "  LinguaMeet - Cloud Deployment" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta
Write-Host ""

# Vérifier que gcloud est installé
Write-Host "[1/6] Vérification de Google Cloud SDK..." -ForegroundColor Cyan
$gcloudPath = Get-Command gcloud -ErrorAction SilentlyContinue

if (-not $gcloudPath) {
    Write-Host ""
    Write-Host "ERREUR: Google Cloud SDK n'est pas installé !" -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez installer Google Cloud SDK:" -ForegroundColor Yellow
    Write-Host "  1. Téléchargez depuis: https://cloud.google.com/sdk/docs/install" -ForegroundColor White
    Write-Host "  2. Installez le package" -ForegroundColor White
    Write-Host "  3. Redémarrez votre terminal" -ForegroundColor White
    Write-Host "  4. Réessayez ce script" -ForegroundColor White
    Write-Host ""
    Write-Host "OU installez via Chocolatey:" -ForegroundColor Yellow
    Write-Host "  choco install gcloudsdk" -ForegroundColor White
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour ouvrir la page de téléchargement"
    Start-Process "https://cloud.google.com/sdk/docs/install"
    exit 1
}

Write-Host "OK - Google Cloud SDK trouvé" -ForegroundColor Green
Write-Host ""

# Configuration du projet
Write-Host "[2/6] Configuration du projet..." -ForegroundColor Cyan
gcloud config set project $ProjectId --quiet
gcloud config set run/region $Region --quiet
Write-Host "OK - Projet configuré: $ProjectId" -ForegroundColor Green
Write-Host ""

# Vérifier l'authentification
Write-Host "[3/6] Vérification de l'authentification..." -ForegroundColor Cyan
$currentAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null

if (-not $currentAccount) {
    Write-Host "Non authentifié. Lancement de l'authentification..." -ForegroundColor Yellow
    gcloud auth login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Échec de l'authentification" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "OK - Connecté en tant que: $currentAccount" -ForegroundColor Green
}
Write-Host ""

# Activer les APIs
Write-Host "[4/6] Activation des APIs Google Cloud..." -ForegroundColor Cyan
$apis = @("run.googleapis.com", "cloudbuild.googleapis.com", "containerregistry.googleapis.com")
foreach ($api in $apis) {
    Write-Host "  Activation: $api" -ForegroundColor Gray
    gcloud services enable $api --quiet 2>$null
}
Write-Host "OK - APIs activées" -ForegroundColor Green
Write-Host ""

# Demander la SECRET_KEY
Write-Host "[5/6] Configuration de la SECRET_KEY..." -ForegroundColor Cyan
Write-Host ""
$secretKey = Read-Host "Entrez votre SECRET_KEY Django (ou laissez vide pour générer)"

if ([string]::IsNullOrWhiteSpace($secretKey)) {
    Write-Host "Génération d'une nouvelle SECRET_KEY..." -ForegroundColor Yellow
    # Générer une clé aléatoire de 50 caractères
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    $secretKey = -join ((1..50) | ForEach-Object { $chars[(Get-Random -Maximum $chars.Length)] })
    Write-Host "OK - SECRET_KEY générée" -ForegroundColor Green
}
Write-Host ""

# Déploiement
Write-Host "[6/6] Déploiement sur Cloud Run..." -ForegroundColor Cyan
Write-Host "Cela peut prendre 5-10 minutes..." -ForegroundColor Yellow
Write-Host ""

gcloud run deploy $ServiceName `
    --source . `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 1Gi `
    --timeout 3600 `
    --max-instances 10 `
    --set-env-vars "DEBUG=False,SECRET_KEY=$secretKey"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "  DÉPLOIEMENT RÉUSSI !" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    
    # Récupérer l'URL
    Write-Host "Récupération de l'URL..." -ForegroundColor Cyan
    $serviceUrl = gcloud run services describe $ServiceName --region $Region --format="value(status.url)"
    
    if ($serviceUrl) {
        Write-Host ""
        Write-Host "URL de votre application:" -ForegroundColor Yellow
        Write-Host "  $serviceUrl" -ForegroundColor White
        Write-Host ""
        
        # Mise à jour de la sécurité
        Write-Host "Mise à jour des paramètres de sécurité..." -ForegroundColor Cyan
        $hostname = $serviceUrl -replace "https://", ""
        
        gcloud run services update $ServiceName `
            --region $Region `
            --update-env-vars "ALLOWED_HOSTS=$hostname,.run.app,CSRF_TRUSTED_ORIGINS=$serviceUrl" `
            --quiet
        
        Write-Host "OK - Sécurité configurée" -ForegroundColor Green
        Write-Host ""
        
        # Proposer d'ouvrir
        $openBrowser = Read-Host "Ouvrir l'application dans le navigateur ? (O/N)"
        if ($openBrowser -eq "O" -or $openBrowser -eq "o") {
            Start-Process $serviceUrl
        }
        
        Write-Host ""
        Write-Host "Commandes utiles:" -ForegroundColor Cyan
        Write-Host "  Voir les logs:" -ForegroundColor White
        Write-Host "    gcloud run services logs tail $ServiceName --region $Region" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Redéployer:" -ForegroundColor White
        Write-Host "    .\deploy_simple.ps1" -ForegroundColor Gray
        Write-Host ""
    }
    
} else {
    Write-Host ""
    Write-Host "ERREUR: Échec du déploiement" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pour voir les erreurs:" -ForegroundColor Yellow
    Write-Host "  gcloud builds list --limit 5" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "Terminé !" -ForegroundColor Green
Write-Host ""
