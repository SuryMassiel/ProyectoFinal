from rest_framework.serializers import ModelSerializer
from APPS.Catalogos.Dependency.models import Dependency

class DependencySerializer(ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['id','CodeDependency','NameDependency', 'Active']
        # fields = '__all__'