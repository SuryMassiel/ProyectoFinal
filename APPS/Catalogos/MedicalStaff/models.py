from django.db import models
from APPS.Catalogos.Person.models import Person
from APPS.Catalogos.Dependency.models import Dependency
from APPS.Catalogos.Charges.models import Charges

# Create your models here.
class MedicalStaff(models.Model):
    IdPerson = models.ForeignKey(Person, on_delete=models.RESTRICT)
    IdDependency = models.ForeignKey(Dependency, on_delete=models.RESTRICT)
    IdCharges = models.ForeignKey(Charges, on_delete=models.RESTRICT)
    CodeMedicalStaff = models.CharField(max_length=10, null=False)
    Active = models.BooleanField(default=True)

    class Meta:
        db_table = 'MedicalStaff'


    def __str__(self):
        return self.CodeMedicalStaff


