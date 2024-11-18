from rest_framework.serializers import ModelSerializer
from APPS.Movimientos.PediatricAppointment.models import PediatricAppointment

class PediatricAppointmentSerializer(ModelSerializer):
    class Meta:
        model = PediatricAppointment
        fields = ['id','MedicalStaffId','CodePediatricAppointment','IdPatients','Reason','State', 'DateTime', 'Active']
       # fields = '__all__'