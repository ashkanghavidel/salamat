from django.conf.urls import url

from patient import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^create/$', views.CreatePatient.as_view()),
]