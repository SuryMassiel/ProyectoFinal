from rest_framework.routers import DefaultRouter
from APPS.Catalogos.Charges.API.ChargesAPI import ChargesViewSet

routerCharges = DefaultRouter()

routerCharges.register(prefix='Charges', basename='Charges', viewset=ChargesViewSet)
