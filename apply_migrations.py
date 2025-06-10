import sys
import django
from django.conf import settings
from django.core.management.commands import migrate, showmigrations
from io import StringIO
from django.core.management import call_command

# Setup Django
django.setup()

def check_migrations():
    """Check if there are any unapplied migrations."""
    # Redirect stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    # Run showmigrations command
    call_command('showmigrations')
    
    # Get output
    output = mystdout.getvalue()
    
    # Reset stdout
    sys.stdout = old_stdout
    
    # Check if there are any unapplied migrations
    if '[ ]' in output:
        print("There are unapplied migrations:")
        print(output)
        return False
    else:
        print("All migrations have been applied.")
        return True

def apply_migrations():
    """Apply all migrations."""
    print("Applying migrations...")
    call_command('migrate')
    print("Migrations applied.")

if __name__ == "__main__":
    if not check_migrations():
        apply_migrations()
        check_migrations()
    
    # Always exit with success
    sys.exit(0)
