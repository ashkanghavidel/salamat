from django.shortcuts import render
from django.http import HttpResponse
from doctor.models import *
from doctor.views import get_week_range
import datetime


def show_request(request,requestType):
    """

    :param request:
    :param requestType: reject , accept , remain
    :return: visits that have been reject or accept or not inspected by doctor
    """
    week_range = get_week_range(datetime.date.today())
    today = week_range[0]
    next_week = week_range[1]
    visit_time_interval_maps = VisitTimeIntervalMap.objects.filter(patient__user=request.user,visitTimeInterval__dailyTimeTable__date__range=[today,next_week])
    if requestType == 'accepted':
        visit_time_interval_maps = visit_time_interval_maps.filter(status=True,checked=True)
    elif requestType == 'rejected':
        visit_time_interval_maps = visit_time_interval_maps.filter(status=False, checked=True)
    elif requestType == 'remained':
        visit_time_interval_maps = visit_time_interval_maps.filter(status=False, checked=False)
    return render(request,'patient/patient-requests.html',{'visitTimeIntervalMaps': visit_time_interval_maps})


def show_visits_payment_status(request):
    """

    :param request:
    :return: cash flow of  visits that have been held by doctor and patient
    """
    visits_payment = VisitPayment.objects.filter(visitTimeIntervalMap__patient__user=request.user,visitTimeIntervalMap__checked=True,visitTimeIntervalMap__status=True,visitTimeIntervalMap__isDone=True)
    return render(request, 'patient/payment-status.html',{'visits_payment': visits_payment})


def pay_for_visit(request):
    """

    :param request:
    :return: patient can pay for a visit that has been held
    """
    visit_payment_id = request.POST['visit-payment-id']
    visit_payment = VisitPayment.objects.get(pk=visit_payment_id)
    visit_payment.status = True
    visit_payment.save()
    return HttpResponse(status=200)
