import datetime
from collections import OrderedDict
from datetime import timedelta
from doctor.models import *
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.models import User


def time(request):
    return render(request, 'doctor/time-table.html', {})


### our search algorithm is very simple. whatever the user gives the searcher,
### the searcher simply do the "and" operation with the search informations given.
def search(request):
    search_is_done = False
    if request.method == 'POST':
        expertise = request.POST['degree-title']
        address = request.POST['office-address']
        insurance_name = request.POST['insurance']
        if expertise:
            doctors = Doctor.objects.filter(doctorDegree=DoctorDegree.objects.filter(degree=expertise).first())
            if address:
                doctors = doctors.filter(office__address=address)
            if insurance_name:
                doctors = doctors.filter(insurance__name=insurance_name)
        if not expertise and address:
            doctors = Doctor.objects.filter(office__address=address)
            if insurance_name:
                doctors = doctors.filter(insurance__name=insurance_name)
        if not expertise and not address and insurance_name:
            doctors = Doctor.objects.filter(insurance__name=insurance_name)
        if not address and not expertise and not insurance_name:
            doctors = Doctor.objects.all()
        search_is_done = True
        return render(request, 'doctor/search.html', {'doctors': doctors, 'search_is_done': search_is_done})
    return render(request, 'doctor/search.html', {'search_is_done': search_is_done})


def next_or_previous_account_time_table(request, doctor_user_name, next_or_previous_date):
    week_range = get_week_range(datetime.datetime.strptime(next_or_previous_date, '%Y-%b-%d'))
    first_day_of_week = week_range[0]
    last_day_of_week = week_range[1]
    next_week_first_day = first_day_of_week + datetime.timedelta(days=7)
    previous_week_first_day = first_day_of_week - datetime.timedelta(days=7)
    daily_times_in_week = list(DailyTimeTable.objects.filter(date__range=[first_day_of_week, last_day_of_week],
                                                             doctor__user__username=doctor_user_name))
    visit_dict = {day: VisitTimeInterval.objects.filter(dailyTimeTable=day) for day in daily_times_in_week}
    visit_dict = OrderedDict(sorted(visit_dict.items(), key=lambda t: t[0].date))
    return render(request, 'doctor/time-table.html',
                  {'visitDic': visit_dict, 'next_week_first_day': next_week_first_day,
                   'previous_week_first_day': previous_week_first_day, 'doctor_user_name': doctor_user_name})


def profile_interface(request, doctor_user_name):
    user = User.objects.get(username=doctor_user_name)
    doctor = Doctor.objects.get(user=user)
    try:
        patient_rate = PatientRate.objects.get(doctor=doctor)
    except PatientRate.DoesNotExist:
        patient_rate = None
    return render(request, 'doctor/profile-interface.html', {'doctor': doctor, 'patient_rate': patient_rate})


def get_patients_comments(request, doctor_user_name):
    user = User.objects.get(username=doctor_user_name)
    doctor = Doctor.objects.get(user=user)
    patients_comments = PatientComment.objects.filter(doctor=doctor)
    return render(request, 'doctor/patients-comments.html', {'patients_comments': patients_comments})


def get_week_range(date):
    """Find the first/last day of the week for the given day.
    Assuming weeks start on Sunday and end on Saturday.

    Returns a tuple of ``(start_date, end_date)``.

    """
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()

    # Find the first day of the week.
    if dow == 6:
        # Since we want to start with Sunday, let's test for that condition.
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = date - timedelta(days=((dow + 1) % 7))

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + timedelta(days=6)

    return [start_date, end_date]
