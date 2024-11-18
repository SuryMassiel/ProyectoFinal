from rest_framework.serializers import ModelSerializer
from APPS.Catalogos.Tutors.models import Tutors


class TutorsSerializer(ModelSerializer):
    class Meta:
        model = Tutors
        fields = ['id','IdPerson','CodeTutor','Occupation','Active']
       # fields = '__all__'