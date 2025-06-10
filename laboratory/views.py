from django.shortcuts import render, get_object_or_404, redirect
from patients.models import Patient
from .models import LabTest
from .forms import LabTestForm

def lab_dashboard(request):
    """
    Main dashboard for the laboratory module.
    Shows recent lab tests and provides access to laboratory functions.
    """
    recent_tests = []
    try:
        recent_tests = LabTest.objects.all().order_by('-specimen_collection_datetime')[:10]
    except Exception as e:
        # Handle any database errors gracefully
        print(f"Error fetching lab tests: {e}")
    
    return render(request, 'laboratory/dashboard.html', {
        'recent_tests': recent_tests
    })

def dispense(request):
    patient_id = request.GET.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id) if patient_id else None
    
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            LabTest.objects.create(
                patient=patient,
                specimen_collection_datetime=data['specimen_collection_datetime'],
                specimen_type=data['specimen_type'],
                uds=data['uds'],
                uds_substances=','.join(data['uds_substances']),
                urine_creatinine=data['urine_creatinine'],
                urine_ph=data['urine_ph'],
                bac=data['bac'],
                lft_alt=data['lft_alt'],
                lft_ast=data['lft_ast'],
                lft_alp=data['lft_alp'],
                lft_bilirubin=data['lft_bilirubin'],
                hep_c_ab=data['hep_c_ab'],
                hep_c_rna=data['hep_c_rna'],
                hep_b_surface=data['hep_b_surface'],
                hiv_ab=data['hiv_ab'],
                hiv_viral_load=data['hiv_viral_load'],
                cbc_hb=data['cbc_hb'],
                cbc_hct=data['cbc_hct'],
                cbc_wbc=data['cbc_wbc'],
                cbc_platelets=data['cbc_platelets'],
                serum_creatinine=data['serum_creatinine'],
                egfr=data['egfr'],
                sodium=data['sodium'],
                potassium=data['potassium'],
                chloride=data['chloride'],
                bicarbonate=data['bicarbonate'],
                blood_glucose=data['blood_glucose'],
                tsh=data['tsh'],
                pregnancy_test=data['pregnancy_test'],
                syphilis_screen=data['syphilis_screen'],
                tb_screen=data['tb_screen'],
                buprenorphine_levels=data['buprenorphine_levels'],
                methadone_levels=data['methadone_levels'],
                naltrexone_levels=data['naltrexone_levels'],
                test_result_status=data['test_result_status'],
                lab_comments=data['lab_comments']
            )
            return render(request, 'laboratory/dispense.html', {
                'form': form, 
                'patient_id': patient_id,
                'success': True
            })
    else:
        form = LabTestForm()
    
    return render(request, 'laboratory/dispense.html', {
        'form': form,
        'patient_id': patient_id
    })
