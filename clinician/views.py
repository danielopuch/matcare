from django.shortcuts import render
from django.utils import timezone
from patients.models import Patient
from .models import LabTestRequestForm
from datetime import datetime

def vitals(request):
    patient_id = request.GET.get('patient_id')
    if request.method == 'POST':
        lab_request_form = LabTestRequestForm(request.POST)
        if lab_request_form.is_valid():
            # Process the lab request
            return render(request, 'clinician/vitals.html', {
                'lab_request_form': lab_request_form,
                'patient_id': patient_id,
                'success': True
            })
    else:
        lab_request_form = LabTestRequestForm()
    
    return render(request, 'clinician/vitals.html', {
        'lab_request_form': lab_request_form,
        'patient_id': patient_id
    })

def queue(request):
    now = timezone.now()
    # Only show patients with a queue_timestamp (i.e., in the queue)
    patients = Patient.objects.exclude(queue_timestamp=None).order_by('-queue_timestamp')
    patient_snippets = []
    for p in patients:
        # Calculate age
        age = None
        if p.date_of_birth:
            age = now.year - p.date_of_birth.year - ((now.month, now.day) < (p.date_of_birth.month, p.date_of_birth.day))
        # Calculate waiting time in minutes
        waiting_time = int((now - p.queue_timestamp).total_seconds() // 60) if p.queue_timestamp else 0
        # BMI
        bmi = None
        if p.weight and p.height:
            try:
                bmi = round(float(p.weight) / ((float(p.height)/100) ** 2), 1)
            except Exception:
                bmi = None
        # BP
        bp = p.blood_pressure if hasattr(p, 'blood_pressure') else ''
        patient_snippets.append({
            'id': p.id,
            'name': f"{p.first_name} {p.last_name}",
            'age': age,
            'address': p.address,
            'bmi': bmi,
            'bp': bp,
            'waiting_time': waiting_time,
        })
    return render(request, 'clinician/queue.html', {'patients': patient_snippets})
