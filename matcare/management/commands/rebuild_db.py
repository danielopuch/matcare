from django.core.management.base import BaseCommand
import os
import subprocess

class Command(BaseCommand):
    help = 'Rebuilds the database from scratch'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting existing database...'))
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            self.stdout.write(self.style.SUCCESS('Database deleted.'))
        
        self.stdout.write(self.style.WARNING('Running migrations...'))
        subprocess.run(['python', 'manage.py', 'makemigrations'])
        subprocess.run(['python', 'manage.py', 'migrate'])
        
        self.stdout.write(self.style.SUCCESS('Database rebuilt successfully!'))
