from django.conf.urls import url

from doctor import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^time/$', views.time, name='time'),
    url(r'^search/$', views.search, name='search'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/add-time/$', views.account_addtime, name='account'),
    url(r'^create-visit-time-interval/$', views.CreateVisitTimeInterval.as_view()),
    url(r'^account/time-table/$', views.account_time_table, name='account'),
    url(r'^account/edit-information/$', views.account_edit_information, name='account'),

]
