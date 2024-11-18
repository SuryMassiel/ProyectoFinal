from django.contrib import admin
from APPS.Catalogos.Dependency.models import  Dependency

# Register your models here.
@admin.register(Dependency)

class DependencyAdmin(admin.ModelAdmin):
    list_display = ['CodeDependency', 'NameDependency', 'Active']
    search_fields = ['CodeDependency', 'NameDependency']