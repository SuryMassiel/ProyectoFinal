from django.db import models

# Create your models here.
class Person(models.Model):
    IdentityCard = models.CharField(max_length=20, null=True)
    Firstname = models.CharField(max_length=200)
    Middlename = models.CharField(max_length=150, null=True)
    Surnames = models.CharField(max_length=200)
    Sexo = models.CharField(max_length=50)
    Age = models.IntegerField(null=True)
    Phone = models.CharField(max_length=20, null=True)
    Email = models.CharField(max_length=200, null=True)
    Address = models.TextField(max_length=300)


    class Meta:
        db_table = 'Person'



    def __str__(self):
        return self.Firstname