from django.http import HttpResponseRedirect
from doctor.forms import *
from doctor.models import *
from django.shortcuts import render


### with this method the doctor can edit his/her account.
def account_edit_information(request):
    if request.method == 'POST':
        degree_title = request.POST['degreeTitle']
        university = request.POST['university']
        visit_duration = request.POST['visitDuration']
        email = request.POST['email']
        request.user.email = email
        request.user.save()
        doctor = Doctor.objects.get(user=request.user)
        doctor_degree = DoctorDegree.objects.get(doctor=doctor)
        doctor.visitDuration = visit_duration
        doctor_degree.degreeTitle = degree_title
        doctor_degree.university = university
        doctor_degree.save()
        doctor.doctorDegree = doctor_degree
        doctor.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        doctor = Doctor.objects.get(user=request.user)
        return render(request, 'doctor/account.html', {'doctor': doctor})


### with this method the doctor can later enter their phone number, address, and his insurance.
def account_complete_information(request):
    if request.method == 'POST':
        address = request.POST['address']
        telephone = request.POST['telephone']
        deleted_insurance_name = request.POST['removed-insurance']
        doctor = Doctor.objects.get(user=request.user)
        try:
            insurance = Insurance.objects.get(name=deleted_insurance_name)
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
        insurances = Insurance.objects.filter(doctor=doctor)
        return render(request, 'doctor/account.html', {'doctor': doctor, 'insurances': insurances})
