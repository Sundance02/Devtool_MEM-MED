from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View

class daily_medicine_detail(View):
    def get(self, request):
    
        return render(request, 'dailymedicinedetail.html', {"form":1, "teacher":2})

class MedicineAddView(View):
    def get(self, request):
    
        return render(request, 'add-medicine.html', {})