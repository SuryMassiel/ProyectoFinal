from django.db import models

# Create your models here.
class Dependency(models.Model):
    CodeDependency = models.CharField(max_length=5)
    NameDependency = models.CharField(max_length=200)
    Active = models.BooleanField(default=True)


    class Meta:
        db_table = 'Dependency'

    def __str__(self):
        return self.NameDependency