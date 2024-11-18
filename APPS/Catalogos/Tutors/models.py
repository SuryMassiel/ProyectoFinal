from django.db import models
# Create your models here.
from APPS.Catalogos.Person.models import Person

# Create your models here.
class Tutors(models.Model):
    IdPerson = models.ForeignKey(Person, on_delete=models.RESTRICT)
    CodeTutor = models.CharField(max_length=5,null= False)
    Occupation = models.CharField(max_length=100, null=False)
    Active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Tutors'

    def __str__(self):
        return self.CodeTutor
