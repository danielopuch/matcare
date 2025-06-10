from django import forms
from datetime import datetime
from .models import LabTest

UDS_CHOICES = [
    ('Positive', 'Positive (specify substances)'),
    ('Negative', 'Negative'),
    ('Invalid', 'Invalid'),
]
UDS_SUBSTANCES = [
    ('Opioids', 'Opioids'),
    ('Buprenorphine', 'Buprenorphine'),
    ('Methadone', 'Methadone'),
    ('Amphetamines', 'Amphetamines'),
    ('Cocaine', 'Cocaine'),
    ('Cannabis', 'Cannabis'),
    ('Other', 'Other'),
]
HEP_C_AB_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Not Tested', 'Not Tested'),
]
HEP_B_CHOICES = HEP_C_AB_CHOICES
HIV_CHOICES = HEP_C_AB_CHOICES
PREGNANCY_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Not Tested', 'Not Tested'),
]
SYPHILIS_CHOICES = [
    ('Reactive', 'Reactive'),
    ('Non-Reactive', 'Non-Reactive'),
    ('Not Tested', 'Not Tested'),
]
TB_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Indeterminate', 'Indeterminate'),
    ('Not Tested', 'Not Tested'),
]
SPECIMEN_TYPE_CHOICES = [
    ('Urine', 'Urine'),
    ('Blood', 'Blood'),
    ('Saliva', 'Saliva'),
]
RESULT_STATUS_CHOICES = [
    ('Normal', 'Normal'),
    ('Abnormal', 'Abnormal'),
    ('Pending', 'Pending'),
    ('Invalid', 'Invalid'),
]

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        exclude = ['patient']
