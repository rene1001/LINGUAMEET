@echo off
REM =============================================================================
REM Script de Déploiement LinguaMeet sur Google Cloud Run
REM =============================================================================
REM Usage: deploy.bat
REM =============================================================================

echo ================================
echo   LinguaMeet - Cloud Deployment
echo ================================
echo.

REM Vérifier que PowerShell est disponible
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: PowerShell n'est pas disponible
    echo Veuillez installer PowerShell ou utiliser deploy.ps1 directement
    pause
    exit /b 1
)

REM Exécuter le script PowerShell
powershell -ExecutionPolicy Bypass -File "%~dp0deploy.ps1" %*

pause
