from django.contrib import admin
from APPS.Catalogos.MedicalStaff.models import MedicalStaff
# Register your models here.

@admin.register(MedicalStaff)

class MedicalStaffAdmin(admin.ModelAdmin):
    list_display = ['IdPerson','CodeMedicalStaff','IdDependency','IdCharges', 'Active']
    search_fields = ['CodeMedicalStaff']