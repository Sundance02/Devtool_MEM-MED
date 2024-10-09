from django import forms
from .models import *
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelForm, PasswordInput, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from django.db import transaction
from django.contrib.auth.forms import *

from django.db import models
from django import forms

from MEM_MED.models import *

class AddMedicineForm(ModelForm):

    class Meta:
        model = Medication
        fields = ["image",
                  "name",
                  "dosage",
                  "description",
                  "side_effects",
                ]

class AddDailyMedicineForm(ModelForm):

    class Meta:
        model = MedicationSchedule
        fields = ["patient",
                  "medication",
                  "time_to_take",
                  "date_to_take",
                  "before_after",
                  "is_eaten",
                  "quantity",
                  "instructions"]
        widgets = {
            'date_to_take': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicationScheduleForm(forms.ModelForm):
    class Meta:
        model = MedicationSchedule
        fields = ['is_eaten']

    def __init__(self, *args, **kwargs):
        super(MedicationScheduleForm, self).__init__(*args, **kwargs)
        self.fields['is_eaten'].widget = forms.HiddenInput()


class Loginform(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={"class":"block bg-white w-full border border-slate-300 rounded-md w-[350px] py-2 px-4", "placeholder":"ชื่อผู้ใช้..." }))
    password = forms.CharField(widget=PasswordInput(attrs={"class":"block bg-white w-full border border-slate-300 rounded-md w-[350px] py-2 px-4", "placeholder":"รหัสผ่าน..."}))

    class Meta:
        model = User
        fields = [
            "username",
            "password"
        ]
