"""
This script checks and fixes database issues in the MATCARE application.
It will:
1. Check for the existence of the useradmin_userrole table
2. Check for the existence of the patient_id column in laboratory_labtest
3. Create missing tables and columns if needed
"""

import os
import sys
import sqlite3
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
django.setup()

from django.db import connection

def check_table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=%s;",
            [table_name]
        )
        return bool(cursor.fetchone())

def check_column_exists(table_name, column_name):
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        return any(col[1] == column_name for col in columns)

def create_useradmin_tables():
    with connection.cursor() as cursor:
        # Create Role table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS "useradmin_role" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(32) NOT NULL UNIQUE
        );
        """)
        
        # Create UserRole table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS "useradmin_userrole" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" integer NOT NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED,
            "role_id" integer NOT NULL REFERENCES "useradmin_role" ("id") DEFERRABLE INITIALLY DEFERRED,
            UNIQUE ("user_id", "role_id")
        );
        """)
        
        # Insert default roles
        roles = [
            'Triage', 'Counselling', 'Clinician', 'Laboratory', 'Pharmacy', 'HMIS', 'UserAdmin'
        ]
        for role in roles:
            cursor.execute(
                "INSERT OR IGNORE INTO useradmin_role (name) VALUES (%s);",
                [role]
            )

def add_patient_id_to_labtest():
    with connection.cursor() as cursor:
        if not check_column_exists('laboratory_labtest', 'patient_id'):
            cursor.execute("""
            ALTER TABLE laboratory_labtest 
            ADD COLUMN patient_id integer REFERENCES patients_patient(id);
            """)

def main():
    print("Checking and fixing database issues...")
    
    # Check useradmin tables
    useradmin_role_exists = check_table_exists('useradmin_role')
    useradmin_userrole_exists = check_table_exists('useradmin_userrole')
    
    if not useradmin_role_exists or not useradmin_userrole_exists:
        print("Creating missing useradmin tables...")
        create_useradmin_tables()
        print("UserAdmin tables created.")
    else:
        print("UserAdmin tables exist.")
    
    # Check laboratory_labtest patient_id column
    labtest_exists = check_table_exists('laboratory_labtest')
    
    if labtest_exists:
        patient_id_exists = check_column_exists('laboratory_labtest', 'patient_id')
        if not patient_id_exists:
            print("Adding patient_id column to laboratory_labtest...")
            add_patient_id_to_labtest()
            print("Column added.")
        else:
            print("laboratory_labtest.patient_id column exists.")
    else:
        print("laboratory_labtest table does not exist. Run migrations first.")
    
    print("Database check and fix complete.")

if __name__ == "__main__":
    main()
