from django.shortcuts import render
from doctor.models import *
from patient.models import *

# Create your views here.

def main_page(request):
    return render(request, 'main_Side/index.html')
    # try:
    #     user = User.objects.get(username=request.user.username)
    # except User.DoesNotExist:
    #     return render(request, 'main_Side/index.html')
    # try:
    #     doctor = Doctor.objects.get(user=request.user)
    #     return render(request, 'main_Side/index.html',{'doctor':doctor})
    # except Doctor.DoesNotExist:
    #     return render(request, 'main_Side/index.html')
    # # try:
    # #     patient = Patient.objects.get(user=request.user)
    # #     return render(request, 'main_Side/index.html',{'patient':patient})
    # # except Patient.DoesNotExist:

def registerationDirection(request):
    return render(request, 'main_Side/register-direction.html')

def loginDirection(request):
    return render(request, 'main_Side/login-direction.html')