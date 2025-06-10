from django.db import migrations
from django.contrib.auth import get_user_model

def create_default_roles(apps, schema_editor):
    Role = apps.get_model('useradmin', 'Role')
    roles = [
        'Triage',
        'Counselling',
        'Clinician',
        'Laboratory',
        'Pharmacy',
        'HMIS',
        'UserAdmin',
    ]
    for role_name in roles:
        Role.objects.get_or_create(name=role_name)


class Migration(migrations.Migration):
    dependencies = [
        ('useradmin', '0002_create_userrole_tables'),
    ]

    operations = [
        migrations.RunPython(create_default_roles),
    ]
