from rest_framework.serializers import ModelSerializer
from APPS.Movimientos.MedicalHistory.models import MedicalHistory


class MedicalHistorySerializer(ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id','IdPatients','CodeMedicalHistory','Diagnosis','Treatment', 'Forecast', 'Date','WeightPounds','Measure', 'Active']
       # fields = '__all__'