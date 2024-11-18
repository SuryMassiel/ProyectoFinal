
# Register your models here.
from django.contrib import admin
from APPS.Movimientos.PediatricAppointment.models import Patients


# Register your models here.

@admin.register(Patients)

class PatientsAdmin(admin.ModelAdmin):
    list_display = [ 'CodePatient','IdTutors','IdPerson','Birthdate', 'Allergies', 'Active']
    search_fields = ['CodePatient']