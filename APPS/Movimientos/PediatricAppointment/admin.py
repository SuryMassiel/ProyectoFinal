from django.contrib import admin
from APPS.Movimientos.PediatricAppointment.models import PediatricAppointment
# Register your models here.

@admin.register(PediatricAppointment)

class PediatricAppointmentAdmin(admin.ModelAdmin):
    list_display = ['CodePediatricAppointment','MedicalStaffId','IdPatients', 'Reason', 'State', 'DateTime', 'Active']
    search_fields = ['CodePediatricAppointment']
