from rest_framework.routers import DefaultRouter
from APPS.Movimientos.MedicalHistory.API.MedicalHistoryAPI import MedicalHistoryViewSet

routerMedicalHistory = DefaultRouter()

routerMedicalHistory.register(prefix='MedicalHistory', basename='MedicalHistory', viewset=MedicalHistoryViewSet)
