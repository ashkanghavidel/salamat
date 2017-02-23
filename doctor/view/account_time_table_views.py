import datetime
from collections import OrderedDict
from datetime import timedelta
from django.db.models import Q
from django.http import HttpResponseRedirect
from doctor.forms import *
from doctor.models import *
from django.shortcuts import render

from doctor.views import get_week_range


def account(request):
    """
    show overall presentation of doctor account
    """
    daily_time_table_form = DailyTimeTableForm()
    visit_time_interval_time_form = VisitTimeIntervalForm()
    doctor = Doctor.objects.get(user=request.user)
    degree = DoctorDegree.objects.get(doctor=doctor)
    insurances = Insurance.objects.filter(doctor=doctor)
    return render(request, 'doctor/account.html',
                  {'user': request.user, 'doctor': doctor, 'degree': degree, 'daily_time_talbe': daily_time_table_form,
                   'visit_time_interval_time': visit_time_interval_time_form, 'insurances': insurances})

### with this method the doctor can add the times to the table
### for later patients visits.
def account_addtime(request):
    if request.method == 'POST':
        daily_time_table_form = DailyTimeTableForm(data=request.POST)
        visit_time_interval_form = VisitTimeIntervalForm(data=request.POST)
        if daily_time_table_form.is_valid() and visit_time_interval_form.is_valid():
            daily_time_table = daily_time_table_form.save(commit=False)
            doctor = Doctor.objects.get(user=request.user)
            daily_time_table.doctor = doctor
            try:
                daily_time_table = DailyTimeTable.objects.get(doctor=doctor, date=daily_time_table.date)
            except DailyTimeTable.DoesNotExist:
                daily_time_table.save()
            visitTimeInterval = visit_time_interval_form.save(commit=False)
            vti = VisitTimeInterval.objects.filter(Q(dailyTimeTable=daily_time_table),
                                                   Q(Q(startTime__lt=visitTimeInterval.endTime),
                                                     Q(endTime__gt=visitTimeInterval.endTime)) | Q(
                                                       Q(startTime__lt=visitTimeInterval.startTime),
                                                       Q(endTime__gt=visitTimeInterval.startTime)))
            if vti.count() == 0:
                visitTimeInterval.dailyTimeTable = daily_time_table
                visitTimeInterval.save()
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


### with this method the doctor can see the times and user who have got them at the table
def account_time_table(request, doctor_user_name):
    if doctor_user_name == 'this':
        doctor_username = request.user.username
    else:
        doctor_username = doctor_user_name
    week_range = get_week_range(datetime.date.today())
    first_day_of_week = week_range[0]
    last_day_of_week = week_range[1]
    next_week_first_day = first_day_of_week + timedelta(days=7)
    previous_week_first_day = first_day_of_week - timedelta(days=7)
    daily_times_in_week = list(DailyTimeTable.objects.filter(date__range=[first_day_of_week, last_day_of_week],
                                                             doctor__user__username=doctor_username))
    visit_dict = {day: VisitTimeInterval.objects.filter(dailyTimeTable=day) for day in daily_times_in_week}
    visit_dict = OrderedDict(sorted(visit_dict.items(), key=lambda t: t[0].date))
    return render(request, 'doctor/time-table.html',
                  {'visitDic': visit_dict, 'next_week_first_day': next_week_first_day,
                   'previous_week_first_day': previous_week_first_day, 'doctor_user_name': doctor_username})
