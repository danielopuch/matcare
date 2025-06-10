from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('users', '__first__'),  # Depends on the users app being migrated first
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Triage', 'Triage'), ('Counselling', 'Counselling'), ('Clinician', 'Clinician'), ('Laboratory', 'Laboratory'), ('Pharmacy', 'Pharmacy'), ('HMIS', 'HMIS'), ('UserAdmin', 'User Administration')], max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=models.deletion.CASCADE, to='useradmin.role')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to='users.customuser')),
            ],
            options={
                'unique_together': {('user', 'role')},
            },
        ),
    ]
