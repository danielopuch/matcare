from django.db import models
from patients.models import Patient
from django.utils import timezone

# Create your models here.

# LabTest model moved to laboratory.models

class Dispense(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dispenses')
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    instructions = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    next_appointment = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.medication} - {self.dosage} - {self.created_at.strftime('%Y-%m-%d')}"
