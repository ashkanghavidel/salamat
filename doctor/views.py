import datetime
from datetime import timedelta

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from doctor.forms import *
from doctor.models import *
from patient.models import Patient
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
                doctor = Doctor.objects.get(user=request.user)
                # return redirect('/main_Side/Welcome_to_Salamat/',doctor=doctor)
                return render(request, 'main_Side/index.html', {'doctor': doctor})
                # t = loader.get_template('main_Side/index.html')
                # c = {'doctor':doctor}
                # return HttpResponse(t.render(c, request,))
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
        address = request.POST['office-address']
        insuranceName = request.POST['insurance']
        if expertise:
            print(expertise)
            doctors = Doctor.objects.filter(doctorDegree__degreeTitle=expertise)
        if address:
            print(address)
            doctors = doctors.filter(office__address=address)
        if insuranceName:
            print(insuranceName)
            doctors = doctors.filter(insurance__name=insuranceName)
        if not address and not expertise and not insuranceName:
            doctors = Doctor.objects.all()
        # doctors = Doctor.objects.filter(doctorDegree__degreeTitle=expertise,insurance__name=insuranceName,office__address=address)
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
    insurances = Insurance.objects.filter(doctor=doctor)
    return render(request, 'doctor/account.html',
                  {'user': request.user, 'doctor': doctor, 'degree': degree, 'daily_time_talbe': dailyTimeTableForm,
                   'visit_time_interval_time': visitTimeIntervalTimeForm, 'insurances': insurances})


def account_addtime(request):
    if request.method == 'POST':
        dailyTimeTableForm = DailyTimeTableForm(data=request.POST)
        visitTimeIntervalForm = VisitTimeIntervalForm(data=request.POST)
        if dailyTimeTableForm.is_valid() and visitTimeIntervalForm.is_valid():
            dailytimeTable = dailyTimeTableForm.save(commit=False)
            doctor = Doctor.objects.get(user=request.user)
            dailytimeTable.doctor = doctor
            try:
                dailytimeTable = DailyTimeTable.objects.get(doctor=doctor, date=dailytimeTable.date)
            except DailyTimeTable.DoesNotExist:
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


    dailyTimesInWeek = DailyTimeTable.objects.filter(date__range=[today, nextWeek],
                                                     doctor__user__username=request.user.username)
    for da in dailyTimesInWeek:
        print("%s ---------------- " % (da.date))
    visitDict = {day: VisitTimeInterval.objects.filter(dailyTimeTable=day) for day in dailyTimesInWeek}
    return render(request, 'doctor/time-table.html',
                  {'visitDic': visitDict})


def account_edit_information(request):
    if request.method == 'POST':
        degreeTitle = request.POST['degreeTitle']
        university = request.POST['university']
        visitDuration = request.POST['visitDuration']
        email = request.POST['email']
        request.user.email = email
        request.user.save()
        doctor = Doctor.objects.get(user=request.user)
        print(doctor.user.first_name)
        doctorDegree = DoctorDegree.objects.get(doctor=doctor)
        doctor.visitDuration = visitDuration
        doctorDegree.degreeTitle = degreeTitle
        doctorDegree.university = university
        doctorDegree.save()
        doctor.doctorDegree = doctorDegree
        doctor.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        doctor = Doctor.objects.get(user=request.user)
        return render(request, 'doctor/account.html', {'doctor': doctor})


def account_complete_information(request):
    if request.method == 'POST':
        address = request.POST['address']
        telephone = request.POST['telephone']
        addedInsuranceName = request.POST['added-insurance']
        deletedInsuranceName = request.POST['removed-insurance']
        insuranceNames = request.POST['insurance'].split('-')

        doctor = Doctor.objects.get(user=request.user)
        addedInsurance, created = Insurance.objects.get_or_create(name=addedInsuranceName, doctor=doctor)
        try:
            insurance = Insurance.objects.get(name=deletedInsuranceName)
            insurance.delete()
        except Insurance.DoesNotExist:
            pass
        try:
            office = Office.objects.get(telephone=telephone)
        except Office.DoesNotExist:

            office = Office(address=address, telephone=telephone)
            office.save()
            doctor.office = office
            doctor.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        doctor = Doctor.objects.get(user=request.user)
        print(doctor.user.first_name)
        insurances = Insurance.objects.filter(doctor=doctor)
        return render(request, 'doctor/account.html', {'doctor': doctor, 'insurances': insurances})


def profile_interface(request, doctorUserName):
    user = User.objects.get(username=doctorUserName)
    doctor = Doctor.objects.get(user=user)
    return render(request, 'doctor/profile-interface.html', {'doctor': doctor})


def account_time_table_for_patient(request, doctorUserName):
    weekRange = week_range(datetime.date.today())
    today = weekRange[0]
    nextWeek = weekRange[1]
    dailyTimesInWeek = DailyTimeTable.objects.filter(date__range=[today, nextWeek],
                                                     doctor__user__username=doctorUserName)
    visitDict = {day: VisitTimeInterval.objects.filter(dailyTimeTable=day) for day in dailyTimesInWeek}
    return render(request, 'doctor/time-table.html',
                  {'visitDic': visitDict})


def reserve_visit_time(request):
    reserveMap = request.POST['reserve-map']
    print(reserveMap)
    visitTimeInterval = VisitTimeInterval.objects.get(id=reserveMap)
    patient = Patient.objects.get(user=request.user)
    try:
        visitTimeIntervalMap = VisitTimeIntervalMap.objects.get(visitTimeInterval=visitTimeInterval)
        if visitTimeIntervalMap.status == False and visitTimeIntervalMap.checked == True and visitTimeIntervalMap.patient.user.username != patient.user.username:
            visitTimeIntervalMap.status = False
            visitTimeIntervalMap.checked = False
            visitTimeIntervalMap.patient = patient
            visitTimeIntervalMap.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif visitTimeIntervalMap.status == False and visitTimeIntervalMap.checked == False:
            return HttpResponse(status=803)
        elif visitTimeIntervalMap.status == True and visitTimeIntervalMap.checked == True and visitTimeIntervalMap.patient.user.username != patient.user.username:
            return HttpResponse(status=804)
        else:
            return HttpResponse(status=805)
    except VisitTimeIntervalMap.DoesNotExist:
        visitTimeIntervalMap = VisitTimeIntervalMap(patient=patient, visitTimeInterval=visitTimeInterval)
    visitTimeIntervalMap.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_pending_visit_time(request):
    weekRange = week_range(datetime.date.today())
    today = weekRange[0]
    nextWeek = weekRange[1]
    doctor = Doctor.objects.get(user=request.user)
    visitTimeIntervalMaps = VisitTimeIntervalMap.objects.filter(
        visitTimeInterval__dailyTimeTable__date__range=[today, nextWeek],
        visitTimeInterval__dailyTimeTable__doctor=doctor, status=False, checked=False)
    return render(request, 'doctor/pending-request.html', {'visitTimeIntervalMaps': visitTimeIntervalMaps})


def account_accept_or_reject_request(request, responseType):
    visitMapId = request.POST['visit-map-id']
    visitTimeIntervalMap = VisitTimeIntervalMap.objects.get(id=visitMapId)
    if responseType == 'reject':
        visitTimeIntervalMap.status = False
        visitTimeIntervalMap.checked = True
        visitTimeIntervalMap.save()
    else:
        visitTimeIntervalMap.status = True
        visitTimeIntervalMap.checked = True
        visitTimeIntervalMap.visitTimeInterval.status = True
        visitTimeIntervalMap.visitTimeInterval.save()
        visitTimeIntervalMap.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
