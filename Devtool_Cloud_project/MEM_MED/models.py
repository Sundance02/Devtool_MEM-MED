from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    allergies = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

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

class MedicationSchedule(models.Model):

    SCHEDULE_CHOICES = [
        ('ตอนเช้า', 'ตอนเช้า'),
        ('ตอนกลางวัน', 'ตอนกลางวัน'),
        ('ตอนเย็น', 'ตอนเย็น'),
        ('ตอนกลางคืน', 'ตอนกลางคืน')
    ]

    BEFORE_AFTER_MEAL_CHOICES = [
        ('ก่อนอาหาร', 'ก่อนอาหาร'),
        ('หลังอาหาร', 'หลังอาหาร')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)

    time_to_take = models.CharField(
        max_length = 10,
        choices = SCHEDULE_CHOICES
    )

    date_to_take = models.DateField()

    before_after = models.CharField(
        max_length = 10,
        choices = BEFORE_AFTER_MEAL_CHOICES
    )

    is_eaten = models.BooleanField(default=False, null=False)
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
    missed = models.BooleanField(default=False)

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
