from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View

#import จาก forms.py ด้านล่างนี้
from MEM_MED.forms import AddMedicineForm

class daily_medicine_detail(View):
    def get(self, request):
    
        return render(request, 'dailymedicinedetail.html', {"form":1, "teacher":2})

class MedicineAddView(View):
    def get(self, request):

        medication_target = Medication.objects.all()
        form = AddMedicineForm()
        return render(request, 'add-medicine.html', {"medication_target" : medication_target, "form" : form})
    
    def post(self, request):

        medication_target = Medication.objects.all()
        form = AddMedicineForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("add-medicine")
        else:
            return render(request, 'add-medicine.html', {"medication_target" : medication_target, "form" : form})

class MedicineDeleteView(View):

    def get(self, request, pk):
        medication_target = Medication.objects.get(pk=pk)
        medication_target.delete()
        return redirect('add-medicine')

class MedicineEditView(View):

    def get(self, request, pk):
        medication_target = Medication.objects.get(pk=pk)
        form = AddMedicineForm(instance=medication_target)
        return render(request, 'edit-medicine.html', {"form" : form})

    def post(self, request, pk):

        medication_target = Medication.objects.get(pk=pk)
        form = AddMedicineForm(request.POST, request.FILES, instance=medication_target)

        if form.is_valid():
            form.save()
            return redirect("add-medicine")
        else:
            print(form.errors)
            form = AddMedicineForm(instance=medication_target)
            return render(request, 'edit-medicine.html', {"form" : form})