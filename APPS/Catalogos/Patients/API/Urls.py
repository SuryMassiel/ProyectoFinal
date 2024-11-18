from rest_framework.routers import DefaultRouter
from APPS.Catalogos.Patients.API.PatientsAPI import PatientsViewSet

routerPatients = DefaultRouter()

routerPatients.register(prefix='Patients', basename='Patiens', viewset=PatientsViewSet)
