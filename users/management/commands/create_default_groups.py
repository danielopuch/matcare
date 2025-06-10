from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create default user groups and assign permissions for MATCARE roles.'

    def handle(self, *args, **options):
        roles = [
            'System Admin',
            'Triage',
            'Counselling',
            'Clinician',
            'Laboratory',
            'Pharmacy',
            'HMIS',
        ]
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {role}'))
            else:
                self.stdout.write(f'Group already exists: {role}')
        self.stdout.write(self.style.SUCCESS('Default groups created. Assign permissions as needed in Django admin.'))
