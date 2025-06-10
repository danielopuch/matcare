"""
Script to check migration status and apply any pending migrations.
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
django.setup()

from django.db.migrations.recorder import MigrationRecorder
from django.db import connection
from django.apps import apps

def check_migrations():
    """Check all migrations and report their status."""
    print("Checking migration status...")
    
    # Get all migration records from the database
    recorder = MigrationRecorder(connection)
    applied_migrations = recorder.applied_migrations()
    
    # Check each app's migrations
    for app_config in apps.get_app_configs():
        app_label = app_config.label
        print(f"\nApp: {app_label}")
        
        # Skip apps without migrations
        migrations_dir = os.path.join(app_config.path, 'migrations')
        if not os.path.isdir(migrations_dir):
            print("  No migrations directory")
            continue
        
        # List migration files
        migration_files = []
        for name in os.listdir(migrations_dir):
            if name.endswith('.py') and not name.startswith('__'):
                migration_name = name[:-3]  # Remove .py extension
                if migration_name != '__pycache__':
                    migration_files.append(migration_name)
        
        # Compare with applied migrations
        for migration in sorted(migration_files):
            if migration == '__init__':
                continue
                
            status = "Applied" if (app_label, migration) in applied_migrations else "Not Applied"
            print(f"  {migration}: {status}")

def apply_migrations():
    """Apply all pending migrations."""
    print("Applying migrations...")
    from django.core.management import call_command
    call_command('migrate')
    print("Migrations applied.")

if __name__ == "__main__":
    check_migrations()
    
    # Ask if user wants to apply migrations
    choice = input("\nDo you want to apply all pending migrations? (y/n): ")
    if choice.lower() == 'y':
        apply_migrations()
        check_migrations()  # Check again after applying
