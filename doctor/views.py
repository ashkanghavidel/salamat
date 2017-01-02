import datetime
from datetime import timedelta

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from doctor.forms import *
from doctor.models import *
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from doctor.Serializers import CreateVisitTimeIntervalSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status


class CreateVisitTimeInterval(CreateAPIView):
    serializer_class = CreateVisitTimeIntervalSerializer

    def post(self, request, *args, **kwargs):
        print("salam hasan o reza")
        serializer = CreateVisitTimeIntervalSerializer(data=request.data)
        if serializer.is_valid():
            vti = serializer.create(request.data)
            daily_time_table = DailyTimeTable()
            daily_time_table.date = request.POST['date']
            daily_time_table.doctor = Doctor.objects.get(user=request.user)
            daily_time_table.visittimeinterval_set.add(vti)
            daily_time_table.save()
            vti.save()
            return Response(status=status.HTTP_201_CREATED)


def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        doctor_degree_form = DoctorDegreeForm(data=request.POST)

        if user_form.is_valid() and doctor_form.is_valid() and doctor_degree_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            # doctor.save()
            doctor_degree = doctor_degree_form.save()
            doctor.doctorDegree = doctor_degree
            doctor.save()
            return HttpResponseRedirect('/main_Side/Welcome_to_Salamat/')

        else:
            print(user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()
        doctor_degree_form = DoctorDegreeForm()
        # contract_form = ContractForm()

    return render(request, 'doctor/register-login.html',
                  {'user_form': user_form, 'doctor_form': doctor_form, 'doctor_degree_form': doctor_degree_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main_Side/Welcome_to_Salamat/', {'user':request.user})
            else:
                return HttpResponse('register/')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'doctor/register-login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/main_Side/Welcome_to_Salamat')

def time(request):
    return render(request, 'doctor/time-table.html', {})


def search(request):
    search_is_done = False
    if request.method == 'POST':
        expertise = request.POST['degree-title']
        # place = request.POST['place']
        # time = request.POST['time']
        # insurance = request.POST['insurance']
        degree = DoctorDegree.objects.get(degreeTitle=expertise)
        doctors = Doctor.objects.filter(doctorDegree=degree)
        search_is_done = True
        return render(request, 'doctor/search.html', {'doctors': doctors, 'search_is_done': search_is_done})
    return render(request, 'doctor/search.html', {'search_is_done': search_is_done})


@login_required
def account(request):
    # schedule_form = ScheduleForm()
    dailyTimeTableForm = DailyTimeTableForm()
    visitTimeIntervalTimeForm = VisitTimeIntervalForm()
    doctor = Doctor.objects.get(user=request.user)
    degree = DoctorDegree.objects.get(doctor=doctor)
    return render(request, 'doctor/account.html',
                  {'user': request.user, 'doctor': doctor, 'degree': degree, 'daily_time_talbe': dailyTimeTableForm,
                   'visit_time_interval_time': visitTimeIntervalTimeForm})


def account_addtime(request):
    if request.method == 'POST':
        dailyTimeTableForm = DailyTimeTableForm(data=request.POST)
        visitTimeIntervalForm = VisitTimeIntervalForm(data=request.POST)
        if dailyTimeTableForm.is_valid() and visitTimeIntervalForm.is_valid():
            dailytimeTable = dailyTimeTableForm.save(commit=False)
            dailytimeTable.doctor = Doctor.objects.get(user=request.user)
            dailytimeTable.save()
            visitTimeInterval = visitTimeIntervalForm.save(commit=False)
            visitTimeInterval.dailyTimeTable = dailytimeTable
            visitTimeInterval.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # schedule_form = ScheduleForm(data=request.POST)
    # if schedule_form.is_valid():
    #     workingSchedule = schedule_form.save(commit=False)
    #     print(Doctor.objects.filter(user=request.user).first())
    #     workingSchedule.doctor = Doctor.objects.filter(user=request.user).first()
    #     workingSchedule.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def account_time_table(request):
    weekRange = week_range(datetime.date.today())
    today = weekRange[0]
    nextWeek = weekRange[1]
    # print("%s ------------------- %s" % (today,nextWeek))

    dailyTimesInWeek = DailyTimeTable.objects.filter(date__range=[today, nextWeek])
    visitDict = dict((day, VisitTimeInterval.objects.filter(dailyTimeTable=day)) for day in dailyTimesInWeek)
    return render(request, 'doctor/time-table.html',
                  {'visitDic': visitDict})


def account_edit_information(request):
    if request.method == 'POST':
        degreeTitle = request.POST['degreeTitle']
        university = request.POST['university']
        visitDuration = request.POST['visitDuration']
        email = request.POST['email']
        doctor = Doctor.objects.get(user=request.user)
        doctorDegree = DoctorDegree.objects.get(doctor=doctor)
        doctor.visitDuration = visitDuration
        doctor.save()
        doctorDegree.degreeTitle = degreeTitle
        doctorDegree.university = university
        doctorDegree.save()
        request.user.email = email
        request.user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        doctor = Doctor.objects.get(user=request.user)
        return render(request, 'doctor/account.html', {'doctor': doctor})


def week_range(date):
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
        start_date = date - timedelta((dow + 1) % 7)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + timedelta(6)
    # print("%s --------------- %s" % (start_date,end_date))

    return (start_date, end_date)
