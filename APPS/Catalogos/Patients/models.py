from django.db import models
from APPS.Catalogos.Person.models import Person
from APPS.Catalogos.Tutors.models import Tutors

class Patients(models.Model):
    IdPerson = models.ForeignKey(Person, on_delete=models.RESTRICT)
    IdTutors = models.ForeignKey(Tutors, on_delete=models.RESTRICT,verbose_name='IdTutors')
    CodePatient = models.CharField(max_length=6, null=False)
    Birthdate = models.DateField(null=False)
    Allergies = models.TextField(max_length=200, null=True)
    Active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Patients'

    def __str__(self):
        return self.CodePatient