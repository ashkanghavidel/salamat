from django.conf.urls import url

from patient import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^create/$', views.CreatePatient.as_view()),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/edit-information/$', views.account_edit_information, name='account'),
    url(r'^account/show-request/(?P<requestType>\w+)$', views.show_request, name='show_request'),
]
