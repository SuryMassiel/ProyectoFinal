from rest_framework.serializers import ModelSerializer
from APPS.Catalogos.Charges.models import Charges

class ChargesSerializer(ModelSerializer):
    class Meta:
        model = Charges
        fields = ['id','CodeCharge','NameCharges', 'Active']
        # fields = '__all__'