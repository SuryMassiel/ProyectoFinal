from rest_framework.serializers import ModelSerializer
from APPS.Catalogos.MedicalStaff.models import MedicalStaff


class MedicalStaffSerializer(ModelSerializer):
    class Meta:
        model = MedicalStaff
        fields = ['id','IdPerson','IdDependency','IdCharges', 'CodeMedicalStaff', 'Active']
       # fields = '__all__'