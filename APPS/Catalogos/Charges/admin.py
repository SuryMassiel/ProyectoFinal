
from django.contrib import admin

# Register your models here.
from APPS.Catalogos.Charges.models import Charges
@admin.register(Charges)

class ChargesAdmin(admin.ModelAdmin):
    list_display = ['CodeCharge', 'NameCharges', 'Active']
    search_fields = ['CodeCharge', 'NameCharges']