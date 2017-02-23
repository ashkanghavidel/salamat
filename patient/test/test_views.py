from doctor import forms
from patient import forms
from patient.models import *
from doctor.models import *
from django.test import Client
from django.test import TestCase
from patient.view.register_login_views import register
from django.http import HttpResponse
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from mock import patch, MagicMock
from unittest.mock import patch, MagicMock

class CreateVisitTimeIntervalViewTest(TestCase):
    """
    Test the snippet create view
    """
    def setUp(self):
        self.user = User()
        self.factory = RequestFactory()
    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('register'))
        request.user = self.user
        response = register(request)
        self.assertEqual(HttpResponse.status_code, 200)
        # self.assertEqual(HttpResponse.context_data['user'], self.user)
        # self.assertEqual(HttpResponse.context_data['request'], request)


class register_Test(TestCase):
    def setUp(self):
        self.user_form = forms.UserForm(data={'password': 'hello123',
                                    'first_name': 'ali',
                                    'last_name': 'gholi',})
        self.user = self.user_form.save(commit=False)
        self.user.set_password(self.user.password)
        self.patient_form = forms.PatientForm(data={'nationalId':'123123',
                                    'phoneNumber':'234234324',})
        self.patient = self.patient_form.save(commit=False)
        self.user.username = self.patient.nationalId
        self.user.save()
        self.patient.user = self.user
        self.patient.save()

    def test_get(self):
        c = Client()
        this_user = authenticate(username='foo',password='foo')
        response = c.post('/patient/register/',
                          {'user': self.user,'UserForm':self.user_form,'PatientForm':self.patient_form},)
        print('jeeeeeeeeeeeeeeeeeeeeleeeeeeeeeeeeeeeeeee')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient/register-login.html')

class account_edit_information_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='ali')
        self.user = users[0]

    def tearDown(self):
        del self.user
    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.get('/patient/account/edit-information/',
                          {'user':self.user, 'phone-number': '123120909', 'email': 'reza@gmail.com'})
        self.assertEqual(Patient.objects.get(user=self.user).phoneNumber,'123412342')
        self.assertEqual(response.status_code, 200)


class submit_comment_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='ali')
        self.user = users[0]

    def tearDown(self):
        del self.user
    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.post('/patient/account/submit-comment/',
                          {'user':self.user, 'visitpaymentid': '1', 'comment': 'kheily doctore monazaamie'})
        self.assertEqual(PatientComment.objects.get(patient=Patient.objects.get(user=self.user)).text,
                         'kheily doctore monazaamie')
        self.assertEqual(response.status_code, 200)

class rate_doctor_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='ali')
        self.user = users[0]

    def tearDown(self):
        del self.user
    def test_post(self):
        user = self.client.force_login(self.user)
        visit_payment = VisitPayment.objects.get(pk=1)
        visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitpayment=visit_payment)
        response = self.client.post('/patient/account/rate-doctor/',
                          {'user':self.user, 'visitpaymentid': '1', 'rate': 3})
        self.assertEqual(PatientRate.objects.get(doctor=visit_time_interval_map.doctor).lastRate,
                         3)
        self.assertEqual(response.status_code, 200)

class show_request_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='ali')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        visit_payment = VisitPayment.objects.get(pk=1)
        visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitpayment=visit_payment)
        response = self.client.post('/patient/account/show-request/accepted',
                                    {'user': self.user, 'requestType': 'remained'})
        self.assertNotEqual(list(response.context)[0]['visitTimeIntervalMaps'],'not,remained')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'patient/patient-requests.html')

class show_visits_payment_status_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='ali')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        visit_payment = VisitPayment.objects.get(pk=1)
        visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitpayment=visit_payment)
        response = self.client.post('/patient/account/show-payment-status/',
                                    {'user': self.user})
        self.assertNotEqual(list(response.context)[0]['visits_payment'],100)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'patient/payment-status.html')

class pay_for_visit_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='ali')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        visit_payment = VisitPayment.objects.get(pk=1)
        visit_time_interval_map = VisitTimeIntervalMap.objects.get(visitpayment=visit_payment)
        response = self.client.post('/patient/account/pay-for-visit/',
                                    {'user': self.user,'visit-payment-id':1})
        visit_payment = VisitPayment.objects.get(pk=1)
        self.assertEqual(visit_payment.status, True)
        self.assertEqual(response.status_code, 200)

class login_Test(TestCase):
    fixtures = ['info.json']
    def test_post(self):
        client = Client()
        response = client.post('/patient/login/', {'username': 'rk', 'password': 'hello1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'main_Side/index.html')

