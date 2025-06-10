from django.contrib import admin
from .models import LabTest

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'specimen_collection_datetime', 'specimen_type', 'test_result_status')
    search_fields = ('patient__mat_id', 'specimen_type', 'test_result_status')
    list_filter = ('specimen_type', 'test_result_status')
