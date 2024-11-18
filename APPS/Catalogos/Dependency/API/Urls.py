from rest_framework.routers import DefaultRouter
from APPS.Catalogos.Dependency.API.DependencyAPI import DependencyViewSet

routerDependency = DefaultRouter()

routerDependency.register(prefix='Dependency', basename='Dependency', viewset=DependencyViewSet)
