from rest_framework.routers import DefaultRouter
from APPS.Movimientos.PediatricAppointment.API.PediatricAppointmentAPI import PediatricAppointmentViewSet

routerPediatricAppointment = DefaultRouter()

routerPediatricAppointment.register(prefix='PediatricAppointment', basename='PediatricAppointment', viewset= PediatricAppointmentViewSet)
