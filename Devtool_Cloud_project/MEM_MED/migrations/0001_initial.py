# Generated by Django 5.1.1 on 2024-10-08 15:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=255)),
                ('dosage', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('side_effects', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('birthdate', models.DateField()),
                ('allergies', models.TextField(blank=True, null=True)),
                ('medical_history', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicationSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_to_take', models.CharField(choices=[('ตอนเช้า', 'ตอนเช้า'), ('ตอนกลางวัน', 'ตอนกลางวัน'), ('ตอนเย็น', 'ตอนเย็น'), ('ตอนกลางคืน', 'ตอนกลางคืน')], max_length=10)),
                ('date_to_take', models.DateField()),
                ('before_after', models.CharField(choices=[('ก่อนอาหาร', 'ก่อนอาหาร'), ('หลังอาหาร', 'หลังอาหาร')], max_length=10)),
                ('is_eaten', models.BooleanField(default=False)),
                ('quantity', models.CharField(max_length=50)),
                ('instructions', models.TextField(blank=True, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MEM_MED.medication')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MEM_MED.patient')),
            ],
        ),
        migrations.CreateModel(
            name='MedicationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateField()),
                ('time_taken', models.TimeField()),
                ('missed', models.BooleanField(default=False, null=True)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MEM_MED.medication')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MEM_MED.patient')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=255)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MEM_MED.patient')),
            ],
        ),
    ]