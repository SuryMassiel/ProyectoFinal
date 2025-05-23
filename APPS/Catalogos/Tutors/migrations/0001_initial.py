# Generated by Django 4.2.16 on 2024-11-13 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodeTutor', models.CharField(max_length=5)),
                ('Occupation', models.CharField(max_length=100)),
                ('Active', models.BooleanField(default=True)),
                ('IdPerson', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Person.person')),
            ],
            options={
                'db_table': 'Tutors',
            },
        ),
    ]
