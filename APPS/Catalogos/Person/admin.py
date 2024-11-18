from django.contrib import admin
from APPS.Catalogos.Person.models import Person

# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['IdentityCard', 'Firstname', 'Middlename', 'Surnames', 'Sexo', 'Age', 'Phone', 'Email', 'Address']
    search_fields =  ['IdentityCard', 'Firstname', 'Middlename', 'Surnames']