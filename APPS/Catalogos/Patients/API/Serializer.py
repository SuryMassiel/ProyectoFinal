from rest_framework.serializers import ModelSerializer
from APPS.Catalogos.Patients.models import Patients


class PatientsSerializer(ModelSerializer):
    class Meta:
        model = Patients
        fields = ['id','IdPerson','IdTutors','CodePatient','Birthdate','Allergies','Active']
       # fields = '__all__'
