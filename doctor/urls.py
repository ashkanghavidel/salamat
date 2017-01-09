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
    url(r'^account/complete-information/$', views.account_complete_information, name='account'),
    url(r'^profile-interface/(?P<doctorUserName>\w+)/$', views.profile_interface, name='profile_interface'),
    url(r'^time-table/(?P<doctorUserName>\w+)$', views.account_time_table_for_patient, name='patient_time_table'),
    url(r'^reserve-visit-time/$', views.reserve_visit_time, name='reserve_visit_time'),
    url(r'^account/show-pending/$', views.get_pending_visit_time, name='show-pending'),
    url(r'^account/accept-reject-request/(?P<responseType>\w+)$', views.account_accept_or_reject_request, name='account_accept_or_reject_request'),

]
