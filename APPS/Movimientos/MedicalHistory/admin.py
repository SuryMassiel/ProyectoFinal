
from django.contrib import admin
from APPS.Movimientos.MedicalHistory.models import MedicalHistory
@admin.register(MedicalHistory)

class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['CodeMedicalHistory','IdPatients', 'Diagnosis', 'Treatment', 'Forecast', 'Date', 'WeightPounds', 'Measure', 'Active']
    search_fields = ['CodeMedicalHistory']