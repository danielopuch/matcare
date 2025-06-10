from django.shortcuts import render, get_object_or_404, redirect
from patients.models import Patient
from .models import Dispense
from .forms import DispenseForm
from django.contrib import messages

def dispense(request):
    patient_id = request.GET.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id) if patient_id else None
    
    if request.method == 'POST' and patient:
        form = DispenseForm(request.POST)
        if form.is_valid():
            dispense = form.save(commit=False)
            dispense.patient = patient
            dispense.save()
            messages.success(request, 'Medication dispensed successfully.')
            return redirect('patients:dashboard', patient_id=patient.id)
    else:
        form = DispenseForm()
    
    # Get past dispenses for this patient
    past_dispenses = []
    if patient:
        past_dispenses = Dispense.objects.filter(patient=patient).order_by('-created_at')[:5]
    
    return render(request, 'dispensary/dispense.html', {
        'patient': patient,
        'patient_id': patient_id,
        'form': form,
        'past_dispenses': past_dispenses
    })
