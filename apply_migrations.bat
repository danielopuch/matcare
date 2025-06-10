@echo off
cd /d D:\Git\matcare
echo Applying migrations for laboratory app...
python manage.py migrate laboratory
echo.
echo Applying all migrations...
python manage.py migrate
echo.
echo Migration complete.
pause
