
# Create your models here.
from django.db import  models

class Charges(models.Model):
    CodeCharge = models.CharField(max_length=5)
    NameCharges = models.CharField(max_length=100)
    Active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Charges'

    def __str__(self):
        return  self.NameCharges