from rest_framework.routers import DefaultRouter
from APPS.Catalogos.Tutors.API.TutorAPI import TutorsViewSet

routerTutors = DefaultRouter()

routerTutors.register(prefix='Tutors', basename='Tutors', viewset=TutorsViewSet)
