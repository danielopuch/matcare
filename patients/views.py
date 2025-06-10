from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from datetime import date, datetime
from .models import Patient
from django.contrib import messages
from laboratory.models import LabTest  # use only the laboratory LabTest
from treatment.models import *  # adjust import if needed

# Helper to generate MAT ID
import random, string
def generate_mat_id():
    return 'MAT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def triage_home(request):
    return redirect('patients:search_patient')

def patient_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        address_country = request.POST.get('address_country')
        address_district = request.POST.get('address_district')
        address_subcounty = request.POST.get('address_subcounty')
        address_parish = request.POST.get('address_parish')
        address_village = request.POST.get('address_village')
        blood_pressure = request.POST.get('blood_pressure')
        systolic = request.POST.get('systolic')
        diastolic = request.POST.get('diastolic')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        bmi = None
        if weight and height:
            try:
                bmi = round(float(weight) / ((float(height)/100) ** 2), 1)
            except Exception:
                bmi = None
        notes = request.POST.get('notes')
        gender = request.POST.get('gender')
        contact_info = request.POST.get('contact_info')
        # Age validation
        if age and int(age) < 15:
            return render(request, 'patients/patient_register.html', {'error': 'Age must be at least 15 years.'})
        # Gender and phone number validation
        if not gender or not contact_info:
            return render(request, 'patients/patient_register.html', {'error': 'Gender and Phone Number are required.'})
        # Generate MAT ID
        mat_id = generate_mat_id()
        action = request.POST.get('action')
        # Calculate DOB from age if not provided
        if not dob and age:
            try:
                year = date.today().year - int(age)
                dob = date(year, 6, 1)
            except Exception:
                dob = None
        # Save patient (add middle name and vitals)
        patient = Patient.objects.create(            mat_id=mat_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=dob if dob else None,
            gender=request.POST.get('gender', ''),
            contact_info=request.POST.get('phone', ''),
            address=f"{address_country}, {address_district}, {address_subcounty}, {address_parish}, {address_village}",
            medical_history=notes or '',
            emergency_contact_name='',
            emergency_contact_phone='',
            blood_pressure=f"{systolic}/{diastolic}",
            weight=weight,
            height=height,
            notes=f"BMI: {bmi} | " + (notes or '')
        )
        messages.success(request, f'Patient registered successfully! MAT ID: {mat_id}')
        
        # Handle department routing
        department = request.POST.get('department')
        if action == 'register_send_counselling' or department == 'counselling':
            return redirect(f'/treatment/plan/?patient_id={patient.id}')
        elif department == 'clinician':
            from django.utils import timezone
            patient.queue_timestamp = timezone.now()
            patient.save(update_fields=["queue_timestamp"])
            return redirect(f'/clinician/vitals/?patient_id={patient.id}')
        return redirect('patients:register_patient')
    return render(request, 'patients/patient_register.html')

def patient_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Patient.objects.filter(first_name__icontains=query) | Patient.objects.filter(last_name__icontains=query) | Patient.objects.filter(mat_id__icontains=query)
    return render(request, 'patients/patient_search.html', {'results': results, 'query': query, 'title': 'Find MAT Client'})

def patient_dashboard(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Fetch all lab tests for this patient
    lab_tests = []
    try:
        lab_tests = LabTest.objects.filter(patient=patient).order_by('-specimen_collection_datetime')
    except Exception as e:
        print(f"Error fetching lab tests: {e}")
    
    # Fetch all medication dispenses for this patient
    dispenses = []
    next_appointment_date = None
    try:
        from dispensary.models import Dispense
        dispenses = Dispense.objects.filter(patient=patient).order_by('-created_at')
        
        # Get the most recent next appointment date from dispenses
        recent_dispense_with_appointment = dispenses.exclude(next_appointment=None).first()
        if recent_dispense_with_appointment:
            next_appointment_date = recent_dispense_with_appointment.next_appointment
    except Exception as e:
        print(f"Error fetching dispenses: {e}")
    
    # Create comprehensive encounter records with more detailed information
    encounters = []
    
    # Add lab test encounters with detailed test information
    for lt in lab_tests:
        test_details = []
        if lt.uds and lt.uds.lower() != 'not done':
            test_details.append(f"UDS: {lt.uds}")
            if lt.uds_substances:
                test_details.append(f"Substances: {lt.uds_substances}")
        
        if lt.hep_c_ab and lt.hep_c_ab.lower() != 'not done':
            test_details.append(f"Hep C Ab: {lt.hep_c_ab}")
        
        if lt.hiv_ab and lt.hiv_ab.lower() != 'not done':
            test_details.append(f"HIV Ab: {lt.hiv_ab}")
        
        if lt.test_result_status:
            test_details.append(f"Status: {lt.test_result_status}")
        
        details = ", ".join(test_details) if test_details else "No specific test details"
        
        encounters.append({
            'date': lt.specimen_collection_datetime,
            'service': 'Laboratory',
            'details': details,
            'type': 'lab',
            'id': lt.id
        })
    
    # Add dispense encounters with medication details
    for d in dispenses:
        details = f"{d.medication} {d.dosage}, Qty: {d.quantity}"
        if d.instructions:
            details += f", Instructions: {d.instructions[:50]}..."
        
        encounters.append({
            'date': d.created_at,
            'service': 'Pharmacy',
            'details': details,
            'type': 'dispense',
            'id': d.id,
            'next_appointment': d.next_appointment
        })
    
    # Sort encounters by date descending
    encounters = sorted(encounters, key=lambda x: x['date'] or datetime.min, reverse=True)
    
    # Calculate patient age
    age = None
    if patient.date_of_birth:
        today = date.today()
        age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))
    
    # Calculate BMI if weight and height are available
    bmi = None
    if patient.weight and patient.height and patient.height > 0:
        try:
            height_in_meters = float(patient.height) / 100
            bmi = round(float(patient.weight) / (height_in_meters ** 2), 1)
        except:
            bmi = None
    
    return render(request, 'patients/patient_dashboard.html', {
        'patient': patient,
        'encounters': encounters,
        'lab_tests': lab_tests,
        'dispenses': dispenses,
        'next_appointment_date': next_appointment_date,
        'age': age,
        'bmi': bmi
    })
