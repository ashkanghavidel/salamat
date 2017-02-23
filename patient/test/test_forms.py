import datetime
from django.core import mail
from django.conf import settings
from django.core import management
from patient.models import Patient
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from doctor import forms
from patient.forms import *
from django.test import TestCase



class UserFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create(first_name='reza', last_name='rezulu', password='bubu1234')
        data = {'first_name': user.first_name, 'last_name': user.last_name, 'password': user.password}
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = User.objects.create(first_name='reza', last_name='rezulu')
        data = {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username,
                'password': user.password, 'email': user.email}
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

class PatientFormTest(TestCase):
    def test_valid_form(self):
        data = {'nationalId': '123432','phoneNumber':'12351325123'}
        form = PatientForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'address': 'social'}
        form = PatientForm(data=data)
        self.assertFalse(form.is_valid())