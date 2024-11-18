from rest_framework.routers import DefaultRouter
from APPS.Catalogos.MedicalStaff.API.MedicalStaffAPI import MedicalStaffViewSet

routerMedicalStaff = DefaultRouter()

routerMedicalStaff.register(prefix='MedicalStaff', basename='MedicalStaff', viewset=MedicalStaffViewSet)
