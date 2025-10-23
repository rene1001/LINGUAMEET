@echo off
echo Mise a jour du fichier .env...
echo.

REM Créer un nouveau fichier .env avec la configuration complète
(
echo # =============================================================================
echo # Configuration LinguaMeet - Solution GRATUITE Premium
echo # =============================================================================
echo.
echo # -----------------------------------------------------------------------------
echo # PIPELINE GRATUIT PREMIUM ACTIVE
echo # -----------------------------------------------------------------------------
echo.
echo # Activer le pipeline gratuit premium ^(Google STT + Gemini + Google TTS^)
echo USE_FREE_PREMIUM=True
echo.
echo # Gemini API Key ^(GRATUIT - illimite^)
echo GEMINI_API_KEY=AIzaSyAnnhrURu1ACdFFeU7EHaFPto5qtIGQsrs
echo.
echo # Google Cloud Credentials ^(ACTIVE^)
echo GOOGLE_APPLICATION_CREDENTIALS=c:\wamp64\www\LangMeet\LINGUAMEET\credentials\google-cloud-key.json
echo.
echo # =============================================================================
) > .env

echo [OK] Fichier .env mis a jour !
echo.
echo Configuration actuelle :
echo - USE_FREE_PREMIUM : True
echo - GEMINI_API_KEY : Configure
echo - GOOGLE_APPLICATION_CREDENTIALS : Configure
echo.
echo Test de la configuration...
echo.
python test_config.py

pause
