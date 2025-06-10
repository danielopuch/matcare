from django.db import models
import uuid

class Patient(models.Model):
    mat_id = models.CharField(max_length=20, unique=True, default='', editable=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=False)
    contact_info = models.CharField(max_length=100, blank=False)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    # Vitals
    blood_pressure = models.CharField(max_length=20, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    queue_timestamp = models.DateTimeField(null=True, blank=True, help_text='Time patient was sent to clinician queue')
    counselling_queue_timestamp = models.DateTimeField(null=True, blank=True, help_text='Time patient was sent to counselling queue')
    lab_queue_timestamp = models.DateTimeField(null=True, blank=True, help_text='Time patient was sent to laboratory queue')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.mat_id})"
