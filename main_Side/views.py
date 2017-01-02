from django.shortcuts import render

# Create your views here.

def MainPage(request):
    return render(request, 'main_Side/index.html')

def registerationDirection(request):
    return render(request, 'main_Side/register-direction.html')

def loginDirection(request):
    return render(request, 'main_Side/login-direction.html')