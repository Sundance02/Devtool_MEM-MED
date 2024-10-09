from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from calendar import HTMLCalendar
from datetime import datetime
from django.shortcuts import render
import calendar as cale
from datetime import date
#import จาก forms.py ด้านล่างนี้
from MEM_MED.forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def int_to_thai_month(month_num):
    thai_months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", 
        "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", 
        "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    
    if 1 <= month_num <= 12:
        return thai_months[month_num - 1]
    else:
        return "เดือนไม่ถูกต้อง"


class update_medicine_status(View):
    def post(self, request, medicine_id):
        
        medicine = MedicationSchedule.objects.get(pk = medicine_id)
        date = medicine.date_to_take
        print(date.year)
        is_eaten = request.POST.get('is_eaten') == 'on'  # ถ้า checkbox ถูกติ๊กจะได้ True
        medicine.is_eaten = is_eaten
        medicine.save()
            
        return redirect('medicine_sche', year=date.year, month=date.month, day = date.day)


class daily_medicine_detail(View):

    def get(self, request, year, month, day):

        date_to_take = date(year,month,day)
        patient = Patient.objects.get(pk=1) #fix ไว้
        medicine_sche = MedicationSchedule.objects.filter(patient = patient, date_to_take = date_to_take)
        th_month = int_to_thai_month(month) 
        
        form = MedicationScheduleForm()

        #สถานะทานยาโดยรวม
        all_status = True
        for medicine in medicine_sche:
            if medicine.is_eaten is False: 
                all_status = False
                break
        if(not medicine_sche):
            all_status = 2

        #ทานยาเช้า
        medicine_morning = MedicationSchedule.objects.filter(patient = patient, date_to_take = date_to_take, time_to_take = 'ตอนเช้า')
        morning_status = True
        for medicine in medicine_morning:
            if medicine.is_eaten is False: 
                morning_status = False
                break
        if(not medicine_morning):
            morning_status = 2
        

        #ทานยากลางวัน
        medicine_noon = MedicationSchedule.objects.filter(patient = patient, date_to_take = date_to_take, time_to_take = 'ตอนกลางวัน')
        noon_status = True
        for medicine in medicine_noon:
            if medicine.is_eaten is False: 
                noon_status = False
                break
        if(not medicine_noon):
            noon_status = 2

        #ทานยาเย็น
        medicine_eve = MedicationSchedule.objects.filter(patient = patient, date_to_take = date_to_take, time_to_take = 'ตอนเย็น')
        eve_status = True
        for medicine in medicine_eve:
            if medicine.is_eaten is False: 
                eve_status = False
                break
        if(not medicine_eve):
            eve_status = 2
        
        #ทานยาตอนกลางคืน
        medicine_night = MedicationSchedule.objects.filter(patient = patient, date_to_take = date_to_take, time_to_take = 'ตอนกลางคืน')
        night_status = True
        for medicine in medicine_night:
            if medicine.is_eaten is False: 
                night_status = False
                break
        if(not medicine_night):
            night_status = 2


        context = {"patient":patient, "medicine_totake":medicine_sche, "th_month":th_month, 'day':day, "year":year, "all_status":all_status,
                    "morning_status":morning_status, "noon_status":noon_status, "eve_status":eve_status, "night_status":night_status,
                    "medicine_morning":medicine_morning, "medicine_noon":medicine_noon, "medicine_eve":medicine_eve, "medicine_night":medicine_night,
                    "form":form}
        return render(request, 'dailymedicinedetail.html', context)


class calendar(View):
    
    def get(self, request, year=None, month=None):
        log = MedicationLog.objects.all()

        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        else:
            year = int(year)
            month = int(month)

        cal = cale.Calendar()
        month_days = cal.monthdayscalendar(year, month)

        log_dates = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month and log.missed == None}
        log_dates_missed = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month and log.missed == True}
        log_dates_not_missed = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month and log.missed == False}
        
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year


        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        return render(request, 'calendar.html', {
            'month_days': month_days,
            'year': year,
            'month': month,
            'month_name': cale.month_name[month],
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'log_dates': log_dates, 
            'log_dates_missed': log_dates_missed,
            'log_dates_not_missed': log_dates_not_missed
        })

def day_view(request, year, month, day):
    return HttpResponse(f"You clicked on {day}/{month}/{year}")

class PatientListView(View):

    def get(self, request):

        patient_list_target = Patient.objects.all()
        return render(request, 'patient-list.html', {"patient_list_target" : patient_list_target})

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
        

class PatientView(View):

    def get(self, request, pk):
        patient_target = Patient.objects.get(pk=pk)
        
        # ฟังก์ชันคำนวณอายุ
        def calculate_age(birthdate):
            today = datetime.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age

        # คำนวณอายุ
        age = calculate_age(patient_target.birthdate)

        medicationschedule = MedicationSchedule.objects.filter(patient = patient_target)
        
        # เพิ่มอายุใน context
        context = {
            "patient_target": patient_target,
            "age": age,
            "medicationschedule": medicationschedule
        }

        return render(request, 'Patient.html', context)

        

class DailyMedicineAddView(View):
    def get(self, request):

        medication_schedule_target = MedicationSchedule.objects.all()
        form = AddDailyMedicineForm()
        return render(request, 'add-daily-medicine.html', {"medication_schedule_target" : medication_schedule_target, "form" : form})
    
    def post(self, request):

        medication_schedule_target = MedicationSchedule.objects.all()
        form = AddDailyMedicineForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("add-daily-medicine")
        else:
            return render(request, 'add-daily-medicine.html', {"medication_schedule_target" : medication_schedule_target, "form" : form})

class DailyMedicineDeleteView(View):

    def get(self, request, pk):
        medication_schedule_target = MedicationSchedule.objects.get(pk=pk)
        medication_schedule_target.delete()
        return redirect('add-daily-medicine')

class DailyMedicineEditView(View):

    def get(self, request, pk):
        medication_schedule_target = MedicationSchedule.objects.get(pk=pk)
        form = AddDailyMedicineForm(instance=medication_schedule_target)
        return render(request, 'edit-daily-medicine.html', {"form" : form})

    def post(self, request, pk):

        medication_schedule_target = MedicationSchedule.objects.get(pk=pk)
        form = AddDailyMedicineForm(request.POST, instance=medication_schedule_target)

        if form.is_valid():
            form.save()
            return redirect("add-daily-medicine")
        else:
            print(form.errors)
            form = AddDailyMedicineForm(instance=medication_schedule_target)
            return render(request, 'edit-daily-medicine.html', {"form" : form})
