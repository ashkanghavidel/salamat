import datetime
from collections import OrderedDict
from django.http import HttpResponse, HttpResponseRedirect
from doctor.forms import *
from doctor.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render


### the next method is for registering a doctor. we also have a registeration form for
### the Patients.
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

    return render(request, 'doctor/register-login.html',
                  {'user_form': user_form, 'doctor_form': doctor_form, 'doctor_degree_form': doctor_degree_form,
                   'registered': registered})

### We have a user_login to log in the users no_matter they are doctor
### patients.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                print(request)
                doctor = Doctor.objects.get(user=request.user)
                return render(request, 'main_Side/index.html', {'doctor': doctor})
            else:
                return HttpResponse('register/')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'doctor/register-login.html', {})


### this method is written for logging out, but it is obvious that if you
### want to log out, your first be logged in.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/main_Side/Welcome_to_Salamat')
