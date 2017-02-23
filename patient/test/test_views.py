import factory
from doctor import forms
from patient import forms
from patient.models import *
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
        user_form = forms.UserForm(data={'username': 'foo',
                                    'email': 'foo@example.com',
                                    'password': 'foo',
                                    'first_name': 'ali',
                                    'last_name': 'gholi',})
        self.user = user_form.save(commit=False)
        self.user.set_password(self.user.password)
        patient_form = forms.PatientForm(data={'nationalId':'123123'
                                    ,'username': 'foo',
                                    'phoneNumber':'234234324',
                                    'email': 'foo@example.com',
                                    'password1': 'foo',
                                    'first_name': 'ali',
                                    'last_name': 'gholi',})
        self.patient = patient_form.save(commit=False)
        self.user.username = self.patient.nationalId
        self.user.save()
        self.patient.user = self.user
        self.patient.save()

    def test_get(self):
        c = Client()
        this_user = authenticate(username='foo',password='foo')
        response = c.get('/patient/register/',
                          {'user': self.user},)
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
        response = self.client.post('/patient/account/edit-information/',
                          {'user':self.user, 'phone-number': '123120909', 'email': 'reza@gmail.com'})
        self.assertEqual(Patient.objects.get(user=self.user).phoneNumber,'123120909')
        self.assertEqual(response.status_code, 302)












