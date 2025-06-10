@echo off
cd /d D:\Git\matcare
echo ---------------------------------------------
echo MATCARE DATABASE MIGRATION UTILITY
echo ---------------------------------------------
echo.
echo Activating virtual environment...
call env\Scripts\activate.bat
echo.

echo Running laboratory migrations...
python manage.py migrate laboratory
echo.

echo Running all other migrations...
python manage.py migrate
echo.

echo Checking migration status...
python manage.py showmigrations laboratory
echo.

echo Migration process complete.
echo If you still see migration warnings, please run:
echo python fix_laboratory_migrations_direct.py
echo.
echo ---------------------------------------------
echo Press any key to exit...
pause > nul
