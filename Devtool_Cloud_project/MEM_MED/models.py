from django.db import models

from django.db import models
from django.contrib.auth.models import User

# ของ ผู้ป่วย
# 1.หมอนัดหมายผู้ป่วย
# 2.ถึงเวลานัด

# ของ หมอ
# 1.ถึงเวลานัด

class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    allergies = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    expertise = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Medication(models.Model):

    image = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Schedule(models.TextChoices):
        MORNING = 'ตอนเช้า', 'ตอนเช้า'
        AFTERNOON = 'ตอนกลางวัน', 'ตอนกลางวัน'
        EVENING = 'ตอนเย็น', 'ตอนเย็น'
        NIGHT = 'ตอนกลางคืน', 'ตอนกลางคืน'

class Before_After_Meal(models.TextChoices):
        Before = 'ก่อนอาหาร', 'ก่อนอาหาร'
        After = 'หลังอาหาร', 'หลังอาหาร'


class MedicationSchedule(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)

    time_to_take = models.CharField(
        max_length = 10,
        choices = Schedule.choices
    )

    date_to_take = models.DateField()

    before_after = models.CharField(
        max_length = 10,
        choices = Before_After_Meal.choices
    )

    is_eaten = models.BooleanField(default=None, null=True)
    quantity = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication.name} for {self.patient.name} at {self.time_to_take}"

class MedicationLog(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    date_taken = models.DateField()
    time_taken = models.TimeField()
    missed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.patient.name} - {self.medication.name} on {self.date_taken}"

class DoctorAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor_name} on {self.appointment_date}"
