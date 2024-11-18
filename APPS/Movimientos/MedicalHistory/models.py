from django.db import models
# Create your models here.
from APPS.Catalogos.Patients.models import Patients
# Create your models here.
class MedicalHistory(models.Model):
    IdPatients = models.ForeignKey(Patients, on_delete=models.RESTRICT)
    CodeMedicalHistory = models.CharField(max_length=6, null=False)
    Diagnosis = models.TextField(max_length=500, null=False)
    Treatment = models.TextField(max_length=500, null=False)
    Forecast = models.CharField(max_length=200, null=False)
    Date = models.DateField(null=False)
    WeightPounds = models.IntegerField(null = True)
    Measure = models.IntegerField(null =True)
    Active = models.BooleanField(default=True)

    class Meta:
        db_table = 'MedicalHistory'

    def __str__(self):
        return f'{self.CodeMedicalHistory} - {self.Date}'
