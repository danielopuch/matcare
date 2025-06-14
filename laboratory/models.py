from django.db import models
from patients.models import Patient
from django.utils import timezone # Corrected import

class LabTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='lab_tests')
    specimen_collection_datetime = models.DateTimeField(default=timezone.now) # Add default=timezone.now
    specimen_type = models.CharField(max_length=20)
    uds = models.CharField(max_length=20)
    uds_substances = models.CharField(max_length=200, blank=True)
    urine_creatinine = models.FloatField(null=True, blank=True)
    urine_ph = models.FloatField(null=True, blank=True)
    bac = models.FloatField(null=True, blank=True)
    lft_alt = models.FloatField(null=True, blank=True)
    lft_ast = models.FloatField(null=True, blank=True)
    lft_alp = models.FloatField(null=True, blank=True)
    lft_bilirubin = models.FloatField(null=True, blank=True)
    hep_c_ab = models.CharField(max_length=20)
    hep_c_rna = models.CharField(max_length=100, blank=True)
    hep_b_surface = models.CharField(max_length=20)
    hiv_ab = models.CharField(max_length=20)
    hiv_viral_load = models.CharField(max_length=100, blank=True)
    cbc_hb = models.FloatField(null=True, blank=True)
    cbc_hct = models.FloatField(null=True, blank=True)
    cbc_wbc = models.FloatField(null=True, blank=True)
    cbc_platelets = models.FloatField(null=True, blank=True)
    serum_creatinine = models.FloatField(null=True, blank=True)
    egfr = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    chloride = models.FloatField(null=True, blank=True)
    bicarbonate = models.FloatField(null=True, blank=True)
    blood_glucose = models.FloatField(null=True, blank=True)
    tsh = models.FloatField(null=True, blank=True)
    pregnancy_test = models.CharField(max_length=20)
    syphilis_screen = models.CharField(max_length=20)
    tb_screen = models.CharField(max_length=20)
    buprenorphine_levels = models.CharField(max_length=100, blank=True)
    methadone_levels = models.CharField(max_length=100, blank=True)
    naltrexone_levels = models.CharField(max_length=100, blank=True)
    test_result_status = models.CharField(max_length=20)
    lab_comments = models.TextField(blank=True)

    def __str__(self):
        return f"LabTest {self.id} - {self.specimen_collection_datetime}"
