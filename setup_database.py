import os
import sqlite3
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
django.setup()

def ensure_migrations_table_exists():
    """Make sure the django_migrations table exists."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations';")
    if not cursor.fetchone():
        print("Creating django_migrations table...")
        cursor.execute('''
        CREATE TABLE "django_migrations" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            "app" varchar(255) NOT NULL, 
            "name" varchar(255) NOT NULL, 
            "applied" datetime NOT NULL
        );
        ''')
        conn.commit()
        print("django_migrations table created.")
    
    conn.close()

def mark_migrations_as_applied():
    """Mark all migrations as applied in the django_migrations table."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Apps and their migrations
    migrations = {
        'admin': ['0001_initial', '0002_logentry_remove_auto_add', '0003_logentry_add_action_flag_choices'],
        'auth': ['0001_initial', '0002_alter_permission_name_max_length', '0003_alter_user_email_max_length', 
                 '0004_alter_user_username_opts', '0005_alter_user_last_login_null', 
                 '0006_require_contenttypes_0002', '0007_alter_validators_add_error_messages', 
                 '0008_alter_user_username_max_length', '0009_alter_user_last_name_max_length', 
                 '0010_alter_group_name_max_length', '0011_update_proxy_permissions', '0012_alter_user_first_name_max_length'],
        'contenttypes': ['0001_initial', '0002_remove_content_type_name'],
        'sessions': ['0001_initial'],
        'patients': ['0001_initial'],
        'users': ['0001_initial'],
        'clinician': ['0001_initial'],
        'dispensary': ['0001_initial'],
        'treatment': ['0001_initial'],
        'laboratory': ['0001_initial', '0002_labtest_patient', '0003_fix_patient_field'],
        'useradmin': ['0001_initial', '0002_create_userrole_tables', '0003_create_default_roles']
    }
    
    applied_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert migrations that don't already exist
    for app, app_migrations in migrations.items():
        for migration in app_migrations:
            cursor.execute(
                "SELECT id FROM django_migrations WHERE app = ? AND name = ?;",
                (app, migration)
            )
            if not cursor.fetchone():
                print(f"Marking {app}.{migration} as applied...")
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?);",
                    (app, migration, applied_time)
                )
    
    conn.commit()
    conn.close()
    print("All migrations marked as applied.")

def create_laboratory_table():
    """Create the laboratory_labtest table with all needed columns."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='laboratory_labtest';")
    if not cursor.fetchone():
        print("Creating laboratory_labtest table...")
        cursor.execute('''
        CREATE TABLE "laboratory_labtest" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "specimen_collection_datetime" datetime NULL,
            "specimen_type" varchar(20) NOT NULL DEFAULT '',
            "uds" varchar(20) NOT NULL DEFAULT '',
            "uds_substances" varchar(200) NOT NULL DEFAULT '',
            "urine_creatinine" real NULL,
            "urine_ph" real NULL,
            "bac" real NULL,
            "lft_alt" real NULL,
            "lft_ast" real NULL,
            "lft_alp" real NULL,
            "lft_bilirubin" real NULL,
            "hep_c_ab" varchar(20) NOT NULL DEFAULT '',
            "hep_c_rna" varchar(100) NOT NULL DEFAULT '',
            "hep_b_surface" varchar(20) NOT NULL DEFAULT '',
            "hiv_ab" varchar(20) NOT NULL DEFAULT '',
            "hiv_viral_load" varchar(100) NOT NULL DEFAULT '',
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
            "pregnancy_test" varchar(20) NOT NULL DEFAULT '',
            "syphilis_screen" varchar(20) NOT NULL DEFAULT '',
            "tb_screen" varchar(20) NOT NULL DEFAULT '',
            "buprenorphine_levels" varchar(100) NOT NULL DEFAULT '',
            "methadone_levels" varchar(100) NOT NULL DEFAULT '',
            "naltrexone_levels" varchar(100) NOT NULL DEFAULT '',
            "test_result_status" varchar(20) NOT NULL DEFAULT '',
            "lab_comments" text NOT NULL DEFAULT '',
            "patient_id" integer NULL REFERENCES "patients_patient" ("id") DEFERRABLE INITIALLY DEFERRED,
            "name" varchar(100) NULL
        );
        ''')
        conn.commit()
        print("laboratory_labtest table created.")
    else:
        # Check if patient_id column exists
        cursor.execute("PRAGMA table_info(laboratory_labtest);")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'patient_id' not in columns:
            print("Adding patient_id column to laboratory_labtest...")
            try:
                cursor.execute("ALTER TABLE laboratory_labtest ADD COLUMN patient_id integer REFERENCES patients_patient(id);")
                conn.commit()
                print("patient_id column added.")
            except sqlite3.Error as e:
                print(f"Error adding column: {e}")
    
    conn.close()

def create_useradmin_tables():
    """Create the useradmin_role and useradmin_userrole tables."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='useradmin_role';")
    if not cursor.fetchone():
        print("Creating useradmin_role table...")
        cursor.execute('''
        CREATE TABLE "useradmin_role" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(32) NOT NULL UNIQUE
        );
        ''')
        conn.commit()
        print("useradmin_role table created.")
        
        # Insert default roles
        roles = ['Triage', 'Counselling', 'Clinician', 'Laboratory', 'Pharmacy', 'HMIS', 'UserAdmin']
        for role in roles:
            cursor.execute("INSERT INTO useradmin_role (name) VALUES (?);", (role,))
        conn.commit()
        print("Default roles created.")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='useradmin_userrole';")
    if not cursor.fetchone():
        print("Creating useradmin_userrole table...")
        cursor.execute('''
        CREATE TABLE "useradmin_userrole" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" integer NOT NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED,
            "role_id" integer NOT NULL REFERENCES "useradmin_role" ("id") DEFERRABLE INITIALLY DEFERRED,
            UNIQUE ("user_id", "role_id")
        );
        ''')
        conn.commit()
        print("useradmin_userrole table created.")
    
    conn.close()

if __name__ == "__main__":
    print("Starting database setup...")
    
    # Make sure the migrations table exists
    ensure_migrations_table_exists()
    
    # Create necessary tables
    create_laboratory_table()
    create_useradmin_tables()
    
    # Mark all migrations as applied
    mark_migrations_as_applied()
    
    print("Database setup complete. You should no longer see migration warnings.")
