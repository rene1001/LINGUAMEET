@echo off
REM =============================================================================
REM Script d'installation LinguaMeet - Pipeline GRATUIT Premium
REM Pour étudiants - Installe les packages nécessaires
REM =============================================================================

echo.
echo ========================================
echo LinguaMeet - Installation GRATUITE Premium
echo ========================================
echo.
echo Ce script va installer les packages necessaires pour :
echo - Google Speech-to-Text (60 min/mois GRATUIT)
echo - Gemini API (illimite GRATUIT)
echo - Google Text-to-Speech (1M chars/mois GRATUIT)
echo.
echo Cout total : 0 EUR
echo.
pause

echo.
echo [1/5] Verification de l'environnement virtuel...
if not exist "venv\Scripts\activate.bat" (
    echo ERREUR : Environnement virtuel non trouve
    echo Creez-le d'abord avec : python -m venv venv
    pause
    exit /b 1
)

echo [OK] Environnement virtuel trouve
echo.

echo [2/5] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
echo [OK] Environnement virtuel active
echo.

echo [3/5] Mise a jour de pip...
python -m pip install --upgrade pip
echo [OK] pip mis a jour
echo.

echo [4/5] Installation des packages standards...
pip install django daphne channels vosk googletrans==4.0.0rc1 gtts numpy python-dotenv
echo [OK] Packages standards installes
echo.

echo [5/5] Installation des packages GRATUITS Premium...
pip install google-cloud-speech google-cloud-texttospeech google-generativeai
echo [OK] Packages premium installes
echo.

echo ========================================
echo Installation terminee avec succes !
echo ========================================
echo.
echo Prochaines etapes :
echo.
echo 1. Copier .env.example en .env
echo    $ copy .env.example .env
echo.
echo 2. Obtenir cle Gemini (GRATUIT) :
echo    https://makersuite.google.com/app/apikey
echo.
echo 3. Configurer Google Cloud (GRATUIT) :
echo    Suivre SETUP_FREE_PREMIUM.md
echo.
echo 4. Remplir le fichier .env avec vos cles
echo.
echo 5. Tester : python manage.py runserver
echo.
echo Guide complet : GUIDE_ETUDIANT.md
echo ========================================
echo.
pause
