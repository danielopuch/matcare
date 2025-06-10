from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('useradmin', '0001_initial'),  # Update this if you have other migrations
    ]

    operations = [
        # We are removing the RunSQL and relying on Django's ORM to create the tables
        # This ensures better compatibility and consistency
    ]
