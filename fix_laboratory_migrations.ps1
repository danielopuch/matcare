$env:PYTHONPATH = "d:\Git\matcare"
cd d:\Git\matcare

Write-Host "Ensuring database tables are properly created and migrated..." -ForegroundColor Green

# Apply migrations with verbosity
Write-Host "Applying laboratory app migrations with verbosity 2..." -ForegroundColor Yellow
python manage.py migrate laboratory --verbosity 2

# Verify migration status
Write-Host "`nChecking migration status of laboratory app..." -ForegroundColor Yellow
python manage.py showmigrations laboratory

# Checking database schema directly
Write-Host "`nChecking database schema for laboratory_labtest table..." -ForegroundColor Yellow
python -c "
import sqlite3
import os
import sys

db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute(""\"SELECT name FROM sqlite_master WHERE type='table' AND name='laboratory_labtest'\"\"")
    if cursor.fetchone():
        print('laboratory_labtest table exists')
        
        # Get table schema
        cursor.execute('PRAGMA table_info(laboratory_labtest)')
        columns = cursor.fetchall()
        print('\\nTable columns:')
        for col in columns:
            print(f'  {col[1]} ({col[2]})')
        
        # Check for patient_id specifically
        patient_id_col = [col for col in columns if col[1] == 'patient_id']
        if patient_id_col:
            print('\\npatient_id column exists with type:', patient_id_col[0][2])
        else:
            print('\\npatient_id column does NOT exist!')
    else:
        print('laboratory_labtest table does NOT exist!')
    
    conn.close()
else:
    print(f'Database file {db_path} not found')
"

Write-Host "`nForcing migration for laboratory app..." -ForegroundColor Yellow
python manage.py migrate laboratory --fake-initial

Write-Host "`nAll migrations should now be applied." -ForegroundColor Green
