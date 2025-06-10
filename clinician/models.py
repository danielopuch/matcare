from django import forms
from django.db import models

# Create your models here.

class LabTestRequestForm(forms.Form):
    test_choices = [
        ('UDS', 'Urine Drug Screen'),
        ('LFT', 'Liver Function Tests'),
        ('CBC', 'Complete Blood Count'),
        ('HIV', 'HIV Antibody'),
        ('Hepatitis B', 'Hepatitis B Surface Antigen'),
        ('Hepatitis C', 'Hepatitis C Antibody'),
        ('Pregnancy', 'Pregnancy Test'),
        ('Syphilis', 'Syphilis Screen'),
        ('TB', 'Tuberculosis Screen'),
        ('Electrolytes', 'Serum Electrolytes'),
        ('Glucose', 'Blood Glucose'),
        ('TSH', 'Thyroid Stimulating Hormone'),
        ('Other', 'Other'),
    ]
    requested_tests = forms.MultipleChoiceField(choices=test_choices, widget=forms.CheckboxSelectMultiple)
    clinical_notes = forms.CharField(widget=forms.Textarea, required=False)
