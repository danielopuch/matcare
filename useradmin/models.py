from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Role(models.Model):
    ROLE_CHOICES = [
        ('Triage', 'Triage'),
        ('Counselling', 'Counselling'),
        ('Clinician', 'Clinician'),
        ('Laboratory', 'Laboratory'),
        ('Pharmacy', 'Pharmacy'),
        ('HMIS', 'HMIS'),
        ('UserAdmin', 'User Administration'),
    ]
    name = models.CharField(max_length=32, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
