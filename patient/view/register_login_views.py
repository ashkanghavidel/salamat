from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from patient.forms import UserForm,PatientForm
from patient.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        patient_form = PatientForm(data=request.POST)
        user = user_form.save(commit=False)
        user.set_password(user.password)
        patient = patient_form.save(commit=False)
        user.username = patient.nationalId;
        user.save()
        patient.user = user
        patient.save()
        return HttpResponseRedirect('/main_Side/Welcome_to_Salamat/')
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
