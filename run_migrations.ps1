Write-Host "`n---------------------------------------------" -ForegroundColor Cyan
Write-Host "MATCARE DATABASE MIGRATION UTILITY" -ForegroundColor Cyan
Write-Host "---------------------------------------------`n" -ForegroundColor Cyan

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& D:\Git\matcare\env\Scripts\Activate.ps1

Write-Host "`nRunning laboratory migrations..." -ForegroundColor Yellow
python manage.py migrate laboratory

Write-Host "`nRunning all other migrations..." -ForegroundColor Yellow
python manage.py migrate

Write-Host "`nChecking migration status..." -ForegroundColor Yellow
python manage.py showmigrations laboratory

Write-Host "`nMigration process complete." -ForegroundColor Green
Write-Host "If you still see migration warnings, please run:" -ForegroundColor Yellow
Write-Host "python fix_laboratory_migrations_direct.py" -ForegroundColor White -BackgroundColor DarkGray

Write-Host "`n---------------------------------------------" -ForegroundColor Cyan
Write-Host "Press Enter to exit..." -ForegroundColor DarkGray
Read-Host
