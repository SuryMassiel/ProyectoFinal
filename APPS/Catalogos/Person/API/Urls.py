from rest_framework.routers import DefaultRouter
from APPS.Catalogos.Person.API.PersonAPI import PersonViewSet

routerPerson = DefaultRouter()

routerPerson.register(prefix='Person', basename='Person', viewset=PersonViewSet)
