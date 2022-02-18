# Generated by Django 4.0.1 on 2022-02-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0016_patient_bed_alter_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='bed',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='orient',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='prix',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='patient',
            name='prixprop',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8),
        ),
    ]