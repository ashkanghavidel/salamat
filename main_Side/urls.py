from django.conf.urls import url

from main_Side import views

urlpatterns = [
    url(r'^Welcome_to_Salamat/$', views.main_page, name='Welcome_to_Salamat'),
    url(r'^registeration_direction/$', views.registerationDirection, name='registeration_direction'),
    url(r'^login_direction/$', views.loginDirection, name='login_direction'),
]
