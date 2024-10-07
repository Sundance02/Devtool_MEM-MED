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

class daily_medicine_detail(View):

    def get(self, request):
        return render(request, 'dailymedicinedetail.html', {"form":1, "teacher":2})


class calendar(View):
    
    def get(self, request, year=None, month=None):
        log = MedicationLog.objects.all()
    
    # Get current date if year and month are not provided
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        else:
            year = int(year)
            month = int(month)

        # Create a calendar object
        cal = cale.Calendar()
        month_days = cal.monthdayscalendar(year, month)

        # Get all the log dates for the current month
        log_dates = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month}  # Adjust 'log.date' according to your model's field name

        # Previous month
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        # Next month
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        # Pass data to the template
        return render(request, 'calendar.html', {
            'month_days': month_days,
            'year': year,
            'month': month,
            'month_name': cale.month_name[month],
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'log_dates': log_dates,  # Pass the log dates to the template
        })

def day_view(request, year, month, day):
    return HttpResponse(f"You clicked on {day}/{month}/{year}")

class MedicineAddView(View):
    def get(self, request):
    
        return render(request, 'add-medicine.html', {})