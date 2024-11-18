from rest_framework.routers import DefaultRouter
from Seguridad.Usuario.API.UsuarioAPI import UserCreateViewSet

routerUsuario = DefaultRouter()
routerUsuario.register(prefix='Usuario', viewset=UserCreateViewSet, basename='Usuario')
