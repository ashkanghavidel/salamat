import datetime
from django.http import HttpResponse, HttpResponseRedirect
from doctor.models import *
from doctor.views import get_week_range
from patient.models import Patient
from django.shortcuts import render


def reserve_visit_time(request):
    """

    :param request:
    :return: patients can reserve doctor's visits time
    """
    try:
        Doctor.objects.get(user=request.user)
        return HttpResponse('')
    except Doctor.DoesNotExist:
        reserve_map = request.POST['reserve-map']
        visit_time_interval = VisitTimeInterval.objects.get(id=reserve_map)
        patient = Patient.objects.get(user=request.user)
        try:
            visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitTimeInterval=visit_time_interval)
            if visit_time_interval_map.status == False and visit_time_interval_map.checked == True and visit_time_interval_map.patient.user.username != patient.user.username:
                visit_time_interval_map.status = False
                visit_time_interval_map.checked = False
                visit_time_interval_map.patient = patient
                visit_time_interval_map.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif visit_time_interval_map.status == False and visit_time_interval_map.checked == False:
                return HttpResponse(status=803)
            elif visit_time_interval_map.status == True and visit_time_interval_map.checked == True and visit_time_interval_map.patient.user.username != patient.user.username:
                return HttpResponse(status=804)
            else:
                return HttpResponse(status=805)
        except VisitTimeIntervalMap.DoesNotExist:
            visit_time_interval_map = VisitTimeIntervalMap(patient=patient, visitTimeInterval=visit_time_interval, doctor=visit_time_interval.dailyTimeTable.doctor)
            visit_time_interval_map.save()
            visit_payment = VisitPayment(visitTimeIntervalMap=visit_time_interval_map)
            visit_payment.save()
        visit_time_interval_map.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_pending_visit_time(request):
    """

    :param request:
    :return:doctor can see visit request from patients
    """
    week_range = get_week_range(datetime.date.today())
    first_day_of_week = week_range[0]
    last_day_of_week = week_range[1]
    doctor = Doctor.objects.get(user=request.user)
    visit_time_interval_maps = VisitTimeIntervalMap.objects.filter(
        visitTimeInterval__dailyTimeTable__date__range=[first_day_of_week, last_day_of_week],
        doctor=doctor, status=False, checked=False)
    return render(request, 'doctor/pending-request.html', {'visit_time_interval_maps': visit_time_interval_maps})


def set_job_status(request, responseType):
    """

    :param request:
    :param responseType: if visit had been done successfully this param is 'done'
    :return: visits that have been done are specified
    """
    visit_map_id = request.POST['visit-map-id']
    visit_cash_amount = request.POST.get('cash-amount', True)
    visit_time_interval_map = VisitTimeIntervalMap.objects.get(id=visit_map_id)
    visit_payment = VisitPayment.objects.get(visitTimeIntervalMap=visit_time_interval_map)
    if responseType == 'done':
        visit_time_interval_map.isDone = True
        visit_time_interval_map.save()
        visit_payment.cashAmount = visit_cash_amount
        visit_payment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def account_accept_or_reject_request(request, responseType):
    """

    :param request:
    :param responseType: reject or accept
    :return: visits from patients can be accept or reject by doctor
    """
    visit_map_id = request.POST['visit-map-id']
    visit_time_interval_map = VisitTimeIntervalMap.objects.get(id=visit_map_id)
    if responseType == 'reject':
        visit_time_interval_map.status = False
        visit_time_interval_map.checked = True
        visit_time_interval_map.save()
    else:
        visit_time_interval_map.status = True
        visit_time_interval_map.checked = True
        visit_time_interval_map.visitTimeInterval.status = True
        visit_time_interval_map.visitTimeInterval.save()
        visit_time_interval_map.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_accepted_visit(request):
    """

    :param request:
    :return: visits that have been accepted by doctor
    """
    doctor = Doctor.objects.get(user=request.user)
    visit_time_interval_maps = VisitTimeIntervalMap.objects.filter(doctor=doctor,status=True,checked=True,isDone=False)
    return render(request,'doctor/accepted-visit.html',{'visit_time_interval_maps':visit_time_interval_maps})


def get_paid_visit(request):
    """

    :param request:
    :return: visits that have been held by doctor and patient
    """
    doctor = Doctor.objects.get(user=request.user)
    visits_paid = VisitPayment.objects.filter(status=True,visitTimeIntervalMap__doctor=doctor)
    return render(request,'doctor/paid-visit.html',{'visits_paid':visits_paid})
