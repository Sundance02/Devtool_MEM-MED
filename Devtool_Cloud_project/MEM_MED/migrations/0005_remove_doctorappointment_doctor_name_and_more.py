# Generated by Django 5.1.2 on 2024-11-01 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEM_MED', '0004_alter_medicationschedule_is_eaten'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorappointment',
            name='doctor_name',
        ),
        migrations.AlterField(
            model_name='doctorappointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MEM_MED.patient'),
        ),
    ]