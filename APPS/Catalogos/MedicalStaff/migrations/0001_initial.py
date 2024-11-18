# Generated by Django 4.2.16 on 2024-11-13 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Charges', '0001_initial'),
        ('Person', '0001_initial'),
        ('Dependency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodeMedicalStaff', models.CharField(max_length=10)),
                ('Active', models.BooleanField(default=True)),
                ('IdCharges', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Charges.charges')),
                ('IdDependency', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Dependency.dependency')),
                ('IdPerson', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Person.person')),
            ],
            options={
                'db_table': 'MedicalStaff',
            },
        ),
    ]