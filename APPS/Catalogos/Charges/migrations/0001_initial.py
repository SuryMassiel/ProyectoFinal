# Generated by Django 4.2.16 on 2024-11-13 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodeCharge', models.CharField(max_length=5)),
                ('NameCharges', models.CharField(max_length=100)),
                ('Active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Charges',
            },
        ),
    ]
