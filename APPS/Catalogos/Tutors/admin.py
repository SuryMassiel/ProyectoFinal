
from django.contrib import admin
from APPS.Catalogos.Tutors.models import Tutors
@admin.register(Tutors)

class TutorsAdmin(admin.ModelAdmin):
    list_display = ['CodeTutor','IdPerson', 'Occupation', 'Active']
    search_fields = ['CodeTutor']