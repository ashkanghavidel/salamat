from django.http import HttpResponse,HttpResponseRedirect
from patient.models import *
from doctor.models import *
from doctor.views import get_week_range
from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import render


@login_required
def account(request):
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient/account.html',
                  {'user': request.user, 'patient': patient})


def account_edit_information(request):
    if request.method == 'POST':
        phone_number = request.POST['phone-number']
        email = request.POST['email']
        patient = Patient.objects.get(user=request.user)
        patient.phoneNumber = phone_number
        patient.save()
        request.user.email = email
        request.user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        patient = Patient.objects.get(user=request.user)
        return render(request, 'doctor/account.html', {'patient': patient})


def submit_comment(request):
    visit_payment_id = request.POST['visitpaymentid']
    comment_text = request.POST['comment']
    visit_payment = VisitPayment.objects.get(pk=visit_payment_id)
    visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitpayment=visit_payment)
    patient = Patient.objects.get(user=request.user)
    patient_comment = PatientComment(doctor=visit_time_interval_map.doctor,patient=patient,text=comment_text)
    patient_comment.save()
    return HttpResponse(status=200)


def rate_doctor(request):
    visit_payment_id = request.POST['visitpaymentid']
    rate = request.POST['rate']
    visit_payment = VisitPayment.objects.get(pk=visit_payment_id)
    visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitpayment=visit_payment)
    try:
        patient_rate = PatientRate.objects.get(doctor=visit_time_interval_map.doctor)
        patient_rate.lastRate = rate
        total_rate = patient_rate.totalRate
        total_rate = (total_rate + int(rate))/2
        patient_rate.totalRate = total_rate
        patient_rate.save()
    except PatientRate.DoesNotExist:
        patient_rate = PatientRate(doctor=visit_time_interval_map.doctor,lastRate=rate,totalRate=rate)
        patient_rate.save()
    return HttpResponse(status=200)