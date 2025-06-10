from django.shortcuts import render
from patients.models import Patient

def client_list(request):
    clients = Patient.objects.all().order_by('-id')[:100]
    return render(request, 'hmis/client_list.html', {'clients': clients})
