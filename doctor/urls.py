from django.conf.urls import url

from doctor import views
from doctor.view import register_login_views, account_time_table_views, account_information_views, account_visits_views

urlpatterns = [
    url(r'^register/$', register_login_views.register, name='register'),
    url(r'^login/$', register_login_views.user_login, name='login'),
    url(r'^logout/$', register_login_views.user_logout, name='logout'),

    url(r'^account/$', account_time_table_views.account, name='account'),
    url(r'^account/add-time/$', account_time_table_views.account_addtime, name='account'),
    url(r'^account/time-table/(?P<doctor_user_name>\w+)$', account_time_table_views.account_time_table, name='account'),
    url(r'^time-table/(?P<doctor_user_name>\w+)$', account_time_table_views.account_time_table,
        name='patient_time_table'),

    url(r'^account/edit-information/$', account_information_views.account_edit_information, name='account'),
    url(r'^account/complete-information/$', account_information_views.account_complete_information, name='account'),

    url(r'^reserve-visit-time/$', account_visits_views.reserve_visit_time, name='reserve_visit_time'),
    url(r'^account/show-pending/$', account_visits_views.get_pending_visit_time, name='show-pending'),
    url(r'^account/show-accepted-visit/$', account_visits_views.get_accepted_visit, name='show-accepted-visit'),
    url(r'^account/show-paid-visit/$', account_visits_views.get_paid_visit, name='show-paid-visit'),
    url(r'^account/job-status/(?P<responseType>\w+)$', account_visits_views.set_job_status, name='set_job_status'),
    url(r'^account/accept-reject-request/(?P<responseType>\w+)$', account_visits_views.account_accept_or_reject_request,
        name='account_accept_or_reject_request'),

    url(r'^time-table/(?P<doctor_user_name>.+)/(?P<next_or_previous_date>.+)$',
        views.next_or_previous_account_time_table, name='next_or_previous_time_table'),
    url(r'^time/$', views.time, name='time'),
    url(r'^search/$', views.search, name='search'),
    url(r'^profile-interface/(?P<doctor_user_name>\w+)/$', views.profile_interface, name='profile_interface'),
    url(r'^patients-comments/(?P<doctor_user_name>\w+)/$', views.get_patients_comments, name='get_patients_comments'),
]
