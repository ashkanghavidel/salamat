from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from patient.forms import UserForm,PatientForm
from patient.models import *
from doctor.models import *
from doctor.views import week_range
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

import datetime
from datetime import timedelta


from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from patient.Serializers import CreatePatientSerializer, UserRegisterSerializer
from rest_framework import permissions


class CreatePatient(CreateAPIView):
    serializer_class = CreatePatientSerializer
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]

    def post(self, request, *args, **kwargs):
        user_serializer = UserRegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.create(request.data)
            serializer = CreatePatientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(status=status.HTTP_201_CREATED)
            else:
                user.delete()
        return Response(status=status.HTTP_403_FORBIDDEN)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        patient_form = PatientForm(data=request.POST)

        # if user_form.is_valid() and patient_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user.password)

        patient = patient_form.save(commit=False)
        user.username = patient.nationalId;
        user.save()
        patient.user = user
        patient.save()
        return HttpResponseRedirect('/main_Side/Welcome_to_Salamat/')

        # else:
        #     print(user_form.errors, patient_form.errors)

    else:
        user_form = UserForm()
        patient_form = PatientForm()

    return render(request,'patient/register-login.html', {'user_form':user_form, 'patient_form':patient_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                patient = Patient.objects.get(user=request.user)
                # return HttpResponseRedirect('/main_Side/Welcome_to_Salamat/', {'patient': request.user})
                return render(request,'main_Side/index.html',{'patient':patient})
            else:
                return HttpResponse('register/')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'patient/register-login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/main_Side/Welcome_to_Salamat')


@login_required
def account(request):
    # schedule_form = ScheduleForm()
    # dailyTimeTableForm = DailyTimeTableForm()
    # visitTimeIntervalTimeForm = VisitTimeIntervalForm()
    # doctor = Doctor.objects.get(user=request.user)
    # degree = DoctorDegree.objects.get(doctor=doctor)
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient/account.html',
                  {'user': request.user, 'patient': patient})


def account_edit_information(request):
    if request.method == 'POST':
        phoneNumber = request.POST['phone-number']
        email = request.POST['email']
        patient = Patient.objects.get(user=request.user)
        patient.phoneNumber = phoneNumber
        patient.save()
        request.user.email = email
        request.user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        patient = Patient.objects.get(user=request.user)
        return render(request, 'doctor/account.html', {'patient': patient})


def show_request(request,requestType):
    weekRange = week_range(datetime.date.today())
    today = weekRange[0]
    nextWeek = weekRange[1]
    visitTimeIntervalMaps = VisitTimeIntervalMap.objects.filter(patient__user=request.user,visitTimeInterval__dailyTimeTable__date__range=[today,nextWeek])
    if requestType == 'accepted':
        visitTimeIntervalMaps = visitTimeIntervalMaps.filter(status=True,checked=True)
    elif requestType == 'rejected':
        visitTimeIntervalMaps = visitTimeIntervalMaps.filter(status=False, checked=True)
    elif requestType == 'remained':
        visitTimeIntervalMaps = visitTimeIntervalMaps.filter(status=False, checked=False)
    return render(request,'patient/patient-requests.html',{'visitTimeIntervalMaps':visitTimeIntervalMaps})



