# Generated by Django 4.0.1 on 2022-02-14 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0014_alter_patient_currentstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='currentstate',
            field=models.CharField(choices=[('Confirme', 'Confirme'), ('Non conf', 'Non conf'), ('Present', 'Present'), ('Absent', 'Absent')], max_length=15),
        ),
    ]