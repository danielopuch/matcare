$env:PYTHONPATH = "d:\Git\matcare"
cd d:\Git\matcare

# Remove old database
if (Test-Path -Path "db.sqlite3") {
    Remove-Item -Path "db.sqlite3"
    Write-Host "Old database removed."
}

# Recreate database with migrations
Write-Host "Creating new database..."
python manage.py makemigrations
python manage.py migrate

# Create a superuser
Write-Host "Creating superuser..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

# Create default roles
Write-Host "Creating default roles..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
import django
django.setup()
from useradmin.models import Role
roles = ['Triage', 'Counselling', 'Clinician', 'Laboratory', 'Pharmacy', 'HMIS', 'UserAdmin']
for role_name in roles:
    Role.objects.get_or_create(name=role_name)
    print(f'Role {role_name} created.')
"

# Assign UserAdmin role to admin user
Write-Host "Assigning UserAdmin role to admin user..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matcare.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from useradmin.models import Role, UserRole
User = get_user_model()
admin = User.objects.get(username='admin')
admin_role = Role.objects.get(name='UserAdmin')
UserRole.objects.get_or_create(user=admin, role=admin_role)
print('UserAdmin role assigned to admin user.')
"

Write-Host "Database setup complete!"
