from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
