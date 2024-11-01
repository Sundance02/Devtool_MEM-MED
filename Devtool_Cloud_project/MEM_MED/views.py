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
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class RedirectView(View):
    def get(self, request):
        return redirect("login")

class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            current_date = datetime.now()
            year, month = current_date.year, current_date.month

            if user.groups.filter(name="Patient").exists():
                return redirect('calendar', year=year, month=month)
            elif user.groups.filter(name="Doctor").exists():
                return redirect('doc_calendar', year=year, month=month)

        return render(request,'login.html', {"form":form})

class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        logout(request)
        return redirect('login')

class RegisterView(FormView):

    def get(self, request):
        form = RegisterForm()
        #   # เปลี่ยนเส้นทางไปที่หน้า Login หลังจากสมัครเสร็จ
        return render(request, 'register.html', {"form": form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            birthdate = form.cleaned_data['birthdate']
            allergies = form.cleaned_data['allergies']
            medical_history = form.cleaned_data['medical_history']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            patient = Patient.objects.create(
                user=user,
                birthdate=birthdate,
                allergies=allergies,
                medical_history=medical_history,
                name=first_name + last_name
            )
            patient.save()

            return redirect('login')
        return render(request, 'register.html', {"form": form})

class RegisterDoctorView(FormView):

    def get(self, request):
        form = RegisterDoctorForm()
        #   # เปลี่ยนเส้นทางไปที่หน้า Login หลังจากสมัครเสร็จ
        return render(request, 'register-doctor.html', {"form": form})
    
    def post(self, request):
        form = RegisterDoctorForm(request.POST)
        if form.is_valid():
            user = form.save()
            birthdate = form.cleaned_data['birthdate']
            expertise = form.cleaned_data['expertise']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            doctor = Doctor.objects.create(
                user=user,
                birthdate=birthdate,
                expertise=expertise,
                name=first_name + last_name
            )
            doctor.save()

            return redirect('login')
        return render(request, 'register-doctor.html', {"form": form})

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


class update_medicine_status(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_medicationschedule", "MEM_MED.change_medicationschedule"]

    def post(self, request, medicine_id):

        medicine = MedicationSchedule.objects.get(pk = medicine_id)
        date = medicine.date_to_take
        print(date.year)
        is_eaten = request.POST.get('is_eaten') == 'on'  # ถ้า checkbox ถูกติ๊กจะได้ True
        medicine.is_eaten = is_eaten
        medicine.save()

        return redirect('medicine_sche', year=date.year, month=date.month, day = date.day)


class daily_medicine_detail(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_medicationschedule"]

    def get(self, request, year, month, day):

        date_to_take = date(year,month,day)
        present_day = datetime.now().date()
        present_status = False #คนละวันs
        
        print("ปจบ",present_day)
        print("วันหน้าปฏิทิน", date_to_take)

        if(present_day == date_to_take ):
            present_status = True #วันเดียวกัน
        
        print(present_status)

        
        user = User.objects.get(pk=request.user.id)
        patient = Patient.objects.get(user = user) #fix ไว้
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
                    "medicine_morning":medicine_morning, "medicine_noon":medicine_noon, "medicine_eve":medicine_eve, "medicine_night":medicine_night, 'present_day':present_day,
                    "form":form, 'present_status':present_status}
        return render(request, 'dailymedicinedetail.html', context)


class calendar(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_medicationlog"]
    
    def get(self, request, year=None, month=None):
        patient = Patient.objects.get(user = request.user)
        log = MedicationSchedule.objects.filter(patient = patient)

        present_day = datetime.now().date()

        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        else:
            year = int(year)
            month = int(month)

        cal = cale.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        log_dates = {log.date_to_take.day for log in log if log.date_to_take.year == year and log.date_to_take.month == month and log.is_eaten == None and log.date_to_take > present_day}
        log_dates_missed = {log.date_to_take.day for log in log if log.date_to_take.year == year and log.date_to_take.month == month and (log.is_eaten == False or log.is_eaten == None) and log.date_to_take <= present_day}
        log_dates_not_missed = {log.date_to_take.day for log in log if log.date_to_take.year == year and log.date_to_take.month == month and log.is_eaten == True and log.date_to_take <= present_day}

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

        patient_age = year-patient.birthdate.year


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
            'log_dates_not_missed': log_dates_not_missed,
            'patient': patient,
            'patient_age': patient_age
        })
    

class doc_calendar(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_medicationlog"]
    
    def get(self, request, year=None, month=None):
        # log = MedicationSchedule.objects.filter(patient = patient)
        appoint_q = DoctorAppointment.objects.all()

        present_day = datetime.now().date()

        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        else:
            year = int(year)
            month = int(month)

        cal = cale.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        # log_dates = {log.date_to_take.day for log in log if log.date_to_take.year == year and log.date_to_take.month == month and log.is_eaten == None and log.date_to_take > present_day}
        # log_dates_missed = {log.date_to_take.day for log in log if log.date_to_take.year == year and log.date_to_take.month == month and (log.is_eaten == False or log.is_eaten == None) and log.date_to_take <= present_day}
        # log_dates_not_missed = {log.date_to_take.day for log in log if log.date_to_take.year == year and log.date_to_take.month == month and log.is_eaten == True and log.date_to_take <= present_day}

        if appoint_q.exists():
            appointment = {log.appointment_date.day for log in appoint_q if log.appointment_date.year == year and log.appointment_date.month == month and log.appointment_date >= present_day}
            print(appointment)
        else:
            appointment = {}

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



        return render(request, 'doc_calendar.html', {
            'month_days': month_days,
            'year': year,
            'month': month,
            'month_name': cale.month_name[month],
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'log_dates': appointment, 
            # 'log_dates_missed': log_dates_missed,
            # 'log_dates_not_missed': log_dates_not_missed,
            # 'patient': patient,
        })

def day_view(request, year, month, day):
    return HttpResponse(f"You clicked on {day}/{month}/{year}")

class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient"]

    def get(self, request):

        patient_list_target = Patient.objects.all()
        return render(request, 'patient-list.html', {"patient_list_target" : patient_list_target})

class MedicineAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medication", "MEM_MED.add_medication"]

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

class MedicineDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.delete_medication"]

    def get(self, request, pk):
        medication_target = Medication.objects.get(pk=pk)
        medication_target.delete()
        return redirect('add-medicine')

class MedicineEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medication", "MEM_MED.change_medication"]

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

class PatientView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medicationschedule"]

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
    

    # def post(self, request, pk):

class DailyMedicineAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medicationschedule", "MEM_MED.add_medicationschedule"]

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

class DailyMedicineDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.delete_medicationschedule"]

    def get(self, request, pk):
        medication_schedule_target = MedicationSchedule.objects.get(pk=pk)
        medication_schedule_target.delete()
        return redirect('add-daily-medicine')

class DailyMedicineEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medicationschedule", "MEM_MED.change_medicationschedule"]

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


class appointment(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medicationschedule", "MEM_MED.change_medicationschedule"]

    def get(self, request, year, month, day):
        dada = str(year)+"-"+str(month)+"-"+str(day)
        appointment = DoctorAppointment.objects.filter(appointment_date = dada).order_by('appointment_time')
        return render(request, 'appointment.html', {'appoint':appointment, "date":dada})

class add_appointment(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["MEM_MED.view_patient", "MEM_MED.view_medicationschedule", "MEM_MED.change_medicationschedule"]

    def get(self, request, id):
        form = AppointmentForm()
        return render(request, 'addappointment.html', {'form':form})
    
    
    def post(self, request, id):
        form = AppointmentForm(request.POST)
        patient = Patient.objects.get(pk=id)
        doctor = Doctor.objects.get(user=request.user)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = patient
            obj.doctor = doctor
            obj.save()
            return redirect('patient-detail', id)
        
        return render(request, 'addappointment.html', {'form':form})