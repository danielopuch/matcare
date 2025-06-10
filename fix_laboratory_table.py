import os
import sys
import sqlite3
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
django.setup()

def fix_laboratory_labtest_table():
    """
    Directly add the patient_id column to the laboratory_labtest table 
    if it doesn't exist.
    """
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check if the column exists
    cursor.execute("PRAGMA table_info(laboratory_labtest)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'patient_id' not in columns:
        print("Adding patient_id column to laboratory_labtest table...")
        try:
            cursor.execute("ALTER TABLE laboratory_labtest ADD COLUMN patient_id integer REFERENCES patients_patient(id)")
            conn.commit()
            print("Column added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding column: {e}")
    else:
        print("patient_id column already exists in laboratory_labtest table.")
    
    conn.close()

def recreate_laboratory_labtest_table():
    """
    Create a new laboratory_labtest table with all the required fields.
    """
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("Checking if laboratory_labtest table exists...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='laboratory_labtest'")
    table_exists = cursor.fetchone() is not None
    
    if table_exists:
        print("Backing up existing data...")
        cursor.execute("CREATE TABLE IF NOT EXISTS laboratory_labtest_backup AS SELECT * FROM laboratory_labtest")
        print("Dropping existing table...")
        cursor.execute("DROP TABLE laboratory_labtest")
    
    print("Creating new laboratory_labtest table with all fields...")
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
    )
    """)
    
    if table_exists:
        print("Restoring backed up data...")
        try:
            # Get the column names from the backup table
            cursor.execute("PRAGMA table_info(laboratory_labtest_backup)")
            backup_columns = [column[1] for column in cursor.fetchall()]
            
            # Get the column names from the new table
            cursor.execute("PRAGMA table_info(laboratory_labtest)")
            new_columns = [column[1] for column in cursor.fetchall()]
            
            # Find common columns
            common_columns = [col for col in backup_columns if col in new_columns]
            
            # Construct the INSERT query
            columns_str = ", ".join(common_columns)
            sql = f"INSERT INTO laboratory_labtest ({columns_str}) SELECT {columns_str} FROM laboratory_labtest_backup"
            
            cursor.execute(sql)
            print(f"Restored data for {cursor.rowcount} records.")
        except sqlite3.Error as e:
            print(f"Error restoring data: {e}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Starting laboratory_labtest table fix...")
    
    # Try the simple approach first
    fix_laboratory_labtest_table()
    
    # If you need a more comprehensive fix, uncomment the line below
    # recreate_laboratory_labtest_table()
    
    print("Fix completed.")
