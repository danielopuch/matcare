from django.shortcuts import render
from .forms import CounsellingSessionForm

def plan(request):
    patient_id = request.GET.get('patient_id')
    if request.method == 'POST':
        form = CounsellingSessionForm(request.POST)
        if form.is_valid():
            # Save or process form data here
            return render(request, 'treatment/plan.html', {'form': form, 'patient_id': patient_id, 'success': True})
    else:
        form = CounsellingSessionForm()
    return render(request, 'treatment/plan.html', {'form': form, 'patient_id': patient_id})
