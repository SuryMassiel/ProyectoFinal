from django.db import models
from APPS.Catalogos.Patients.models import Patients
from APPS.Catalogos.MedicalStaff.models import MedicalStaff

class PediatricAppointment(models.Model):
    IdPatients = models.ForeignKey(Patients, on_delete=models.RESTRICT)
    MedicalStaffId = models.ForeignKey(MedicalStaff, on_delete=models.RESTRICT)
    CodePediatricAppointment = models.CharField(max_length=10)
    Reason = models.TextField(max_length=500)
    State = models.CharField(max_length=50)
    DateTime = models.DateTimeField(null=False)
    Active = models.BooleanField(default=True)

    class Meta:
        db_table = 'PediatricAppointment'


    def __str__(self):
        return self.CodePediatricAppointment
