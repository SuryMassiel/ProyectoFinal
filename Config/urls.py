"""Config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('',views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from APPS.Catalogos.Charges.API.Urls import routerCharges
from APPS.Catalogos.Dependency.API.Urls import routerDependency
from APPS.Catalogos.Person.API.Urls import routerPerson
from APPS.Movimientos.PediatricAppointment.API.Urls import routerPediatricAppointment
from APPS.Catalogos.MedicalStaff.API.Urls import routerMedicalStaff
from APPS.Catalogos.Patients.API.Urls import routerPatients
from APPS.Movimientos.MedicalHistory.API.Urls import routerMedicalHistory
from APPS.Catalogos.Tutors.API.Urls import routerTutors

from Seguridad.Usuario.API.urls import routerUsuario

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(routerCharges.urls)),
    path('api/', include(routerDependency.urls)),
    path('api/', include(routerPerson.urls)),
    path('api/', include(routerPediatricAppointment.urls)),
    path('api/', include(routerMedicalStaff.urls)),
    path('api/', include(routerPatients.urls)),
    path('api/', include(routerMedicalHistory.urls)),
    path('api/', include(routerTutors.urls)),

    path('api/', include('Seguridad.Usuario.API.router')),

    path('UserCreate', include(routerUsuario.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]