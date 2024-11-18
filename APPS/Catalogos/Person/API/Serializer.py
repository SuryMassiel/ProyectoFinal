from rest_framework.serializers import ModelSerializer
from APPS.Catalogos.Person.models import Person

class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ['id','IdentityCard','Firstname', 'Middlename','Surnames', 'Sexo', 'Age','Phone','Email','Address']
       # fields = '__all__'