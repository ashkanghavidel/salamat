from django.conf.urls import url

from patient import views
from patient.view import register_login_views,account_visits_views


urlpatterns = [
    url(r'^register/$', register_login_views.register, name='register'),
    url(r'^login/$', register_login_views.user_login, name='login'),
    url(r'^logout/$', register_login_views.user_logout, name='logout'),

    url(r'^account/$', views.account, name='account'),
    url(r'^account/edit-information/$', views.account_edit_information, name='account_edit_information'),
    url(r'^account/submit-comment/$', views.submit_comment, name='submit_comment'),
    url(r'^account/rate-doctor/$', views.rate_doctor, name='rate_doctor'),

    url(r'^account/show-request/(?P<requestType>\w+)$', account_visits_views.show_request, name='show_request'),
    url(r'^account/show-payment-status/$', account_visits_views.show_visits_payment_status, name='show_visits_payment_status'),
    url(r'^account/pay-for-visit/$', account_visits_views.pay_for_visit, name='pay_for_visit'),
]

