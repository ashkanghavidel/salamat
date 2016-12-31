from django.shortcuts import render
from django.http import HttpResponse
from patient.forms import UserForm,PatientForm
from django.contrib.auth import authenticate,login
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

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)

            patient = patient_form.save(commit=False)
            user.username = patient.nationalId;
            user.save()
            patient.user = user
            patient.save()
            registered = True

        else:
            print(user_form.errors, patient_form.errors)

    else:
        user_form = UserForm()
        patient_form = PatientForm()

    return render(request,'patient/registerlogin.html', {'user_form':user_form, 'patient_form':patient_form, 'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponse('login done')
            else:
                return HttpResponse('register/')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'patient/registerlogin.html',{})


