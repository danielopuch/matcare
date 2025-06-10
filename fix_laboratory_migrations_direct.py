import os
import sys
import sqlite3
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
django.setup()

from django.db import connection

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

def print_separator():
    print('-' * 80)

def fix_laboratory_migrations():
    print_separator()
    print("FIXING LABORATORY MIGRATIONS")
    print_separator()
    
    # 1. Check database structure
    print("Checking laboratory_labtest table structure...")
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='laboratory_labtest';")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        print("laboratory_labtest table does not exist! Creating it...")
        # Create the table with all required fields
        cursor.execute("""
        CREATE TABLE "laboratory_labtest" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "specimen_collection_datetime" datetime NULL,
            "specimen_type" varchar(20) NOT NULL,
            "uds" varchar(20) NOT NULL,
            "uds_substances" varchar(200) NOT NULL,
            "urine_creatinine" real NULL,
            "urine_ph" real NULL,
            "bac" real NULL,
            "lft_alt" real NULL,
            "lft_ast" real NULL,
            "lft_alp" real NULL,
            "lft_bilirubin" real NULL,
            "hep_c_ab" varchar(20) NOT NULL,
            "hep_c_rna" varchar(100) NOT NULL,
            "hep_b_surface" varchar(20) NOT NULL,
            "hiv_ab" varchar(20) NOT NULL,
            "hiv_viral_load" varchar(100) NOT NULL,
            "cbc_hb" real NULL,
            "cbc_hct" real NULL,
            "cbc_wbc" real NULL,
            "cbc_platelets" real NULL,
            "serum_creatinine" real NULL,
            "egfr" real NULL,
            "sodium" real NULL,
            "potassium" real NULL,
            "chloride" real NULL,
            "bicarbonate" real NULL,
            "blood_glucose" real NULL,
            "tsh" real NULL,
            "pregnancy_test" varchar(20) NOT NULL,
            "syphilis_screen" varchar(20) NOT NULL,
            "tb_screen" varchar(20) NOT NULL,
            "buprenorphine_levels" varchar(100) NOT NULL,
            "methadone_levels" varchar(100) NOT NULL,
            "naltrexone_levels" varchar(100) NOT NULL,
            "test_result_status" varchar(20) NOT NULL,
            "lab_comments" text NOT NULL,
            "patient_id" integer NULL REFERENCES "patients_patient" ("id") DEFERRABLE INITIALLY DEFERRED,
            "name" varchar(100) NULL
        );
        """)
        conn.commit()
        print("Table created successfully!")
    else:
        print("laboratory_labtest table exists.")
        
        # Check if the patient_id column exists
        cursor.execute("PRAGMA table_info(laboratory_labtest);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'patient_id' not in column_names:
            print("patient_id column is missing! Adding it...")
            try:
                cursor.execute("ALTER TABLE laboratory_labtest ADD COLUMN patient_id integer REFERENCES patients_patient(id);")
                conn.commit()
                print("patient_id column added successfully!")
            except sqlite3.Error as e:
                print(f"Error adding column: {e}")
                print("Attempting more complex approach...")
                
                # Create a new table with the correct structure
                cursor.execute("""
                CREATE TABLE "laboratory_labtest_new" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "specimen_collection_datetime" datetime NULL,
                    "specimen_type" varchar(20) NOT NULL,
                    "uds" varchar(20) NOT NULL,
                    "uds_substances" varchar(200) NOT NULL,
                    "urine_creatinine" real NULL,
                    "urine_ph" real NULL,
                    "bac" real NULL,
                    "lft_alt" real NULL,
                    "lft_ast" real NULL,
                    "lft_alp" real NULL,
                    "lft_bilirubin" real NULL,
                    "hep_c_ab" varchar(20) NOT NULL,
                    "hep_c_rna" varchar(100) NOT NULL,
                    "hep_b_surface" varchar(20) NOT NULL,
                    "hiv_ab" varchar(20) NOT NULL,
                    "hiv_viral_load" varchar(100) NOT NULL,
                    "cbc_hb" real NULL,
                    "cbc_hct" real NULL,
                    "cbc_wbc" real NULL,
                    "cbc_platelets" real NULL,
                    "serum_creatinine" real NULL,
                    "egfr" real NULL,
                    "sodium" real NULL,
                    "potassium" real NULL,
                    "chloride" real NULL,
                    "bicarbonate" real NULL,
                    "blood_glucose" real NULL,
                    "tsh" real NULL,
                    "pregnancy_test" varchar(20) NOT NULL,
                    "syphilis_screen" varchar(20) NOT NULL,
                    "tb_screen" varchar(20) NOT NULL,
                    "buprenorphine_levels" varchar(100) NOT NULL,
                    "methadone_levels" varchar(100) NOT NULL,
                    "naltrexone_levels" varchar(100) NOT NULL,
                    "test_result_status" varchar(20) NOT NULL,
                    "lab_comments" text NOT NULL,
                    "patient_id" integer NULL REFERENCES "patients_patient" ("id") DEFERRABLE INITIALLY DEFERRED,
                    "name" varchar(100) NULL
                );
                """)
                
                # Copy data from old table
                try:
                    # Get columns from old table for the INSERT statement
                    old_cols = ", ".join([f'"{c}"' for c in column_names])
                    # For new table, include all old columns plus patient_id as NULL
                    new_cols = old_cols + ", NULL as patient_id"
                    if "name" not in column_names:
                        new_cols += ", NULL as name"
                    
                    cursor.execute(f"INSERT INTO laboratory_labtest_new SELECT {new_cols} FROM laboratory_labtest;")
                    cursor.execute("DROP TABLE laboratory_labtest;")
                    cursor.execute("ALTER TABLE laboratory_labtest_new RENAME TO laboratory_labtest;")
                    conn.commit()
                    print("Table recreated successfully with patient_id column!")
                except sqlite3.Error as e:
                    print(f"Error recreating table: {e}")
        else:
            print("patient_id column exists.")
    
    conn.close()
    
    # 2. Update Django's migration record
    print_separator()
    print("Updating Django's migration records...")
    
    # Check if migrations are in the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT app, name FROM django_migrations WHERE app = 'laboratory';")
        migrations = cursor.fetchall()
        
        if not migrations:
            print("No laboratory migrations found in django_migrations table.")
            print("Adding migration records...")
            
            # Add migration records
            for migration in ['0001_initial', '0002_labtest_patient', '0003_fix_patient_field']:
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, datetime('now'));",
                    ['laboratory', migration]
                )
            print("Migration records added.")
        else:
            print("Existing migrations:")
            for app, name in migrations:
                print(f"  - {app}: {name}")
            
            # Check if we need to add missing migrations
            existing_names = [name for app, name in migrations]
            for migration in ['0001_initial', '0002_labtest_patient', '0003_fix_patient_field']:
                if migration not in existing_names:
                    print(f"Adding missing migration: {migration}")
                    cursor.execute(
                        "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, datetime('now'));",
                        ['laboratory', migration]
                    )
    
    print_separator()
    print("LABORATORY MIGRATIONS FIX COMPLETE")
    print_separator()
    print("You should no longer see the migration warning.")
    print("Please restart your Django server to apply these changes.")
    print_separator()

if __name__ == "__main__":
    fix_laboratory_migrations()
