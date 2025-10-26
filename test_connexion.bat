@echo off
REM Script de test pour vérifier le système d'authentification
REM Usage: test_connexion.bat

echo ========================================
echo Test du Systeme d'Authentification
echo ========================================
echo.

echo 1. Verification de la configuration...
python -c "import django; django.setup(); from django.conf import settings; print('Django version:', django.get_version()); print('DEBUG:', settings.DEBUG); print('SECRET_KEY configuree:', bool(settings.SECRET_KEY)); print('SESSION_ENGINE:', settings.SESSION_ENGINE)"
echo.

echo 2. Verification de la base de donnees...
python manage.py showmigrations
echo.

echo 3. Creation/Verification du superuser admin...
python create_admin.py
echo.

echo 4. Test de connexion (ouverture du navigateur)...
echo.
echo Pour tester:
echo 1. Lancez le serveur: python manage.py runserver
echo 2. Ouvrez: http://localhost:8000/login/
echo 3. Connectez-vous avec: admin / admin123
echo 4. Deconnectez-vous
echo 5. Reconnectez-vous (devrait fonctionner maintenant)
echo.

echo ========================================
echo Test termine !
echo ========================================
pause
