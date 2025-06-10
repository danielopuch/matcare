# LabTestForm and related choices moved to laboratory/forms.py

from django import forms
from .models import Dispense

class DispenseForm(forms.ModelForm):
    class Meta:
        model = Dispense
        fields = ['medication', 'dosage', 'quantity', 'instructions', 'next_appointment', 'notes']
        widgets = {
            'next_appointment': forms.DateInput(attrs={'type': 'date'}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
