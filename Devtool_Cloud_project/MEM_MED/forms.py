from django import forms
from .models import *
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from django.db import transaction

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
        

class MedicationScheduleForm(forms.ModelForm):
    class Meta:
        model = MedicationSchedule
        fields = ['is_eaten']

    def __init__(self, *args, **kwargs):
        super(MedicationScheduleForm, self).__init__(*args, **kwargs)
        self.fields['is_eaten'].widget = forms.HiddenInput()    