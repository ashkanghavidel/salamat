from doctor.forms import *
from django.test import TestCase
from django.contrib.auth.models import User


class UserFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create(first_name='reza', last_name='rezulu', username='Foo', password='bubu1234', email='re@re.com')
        data = {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username, 'password': user.password, 'email': user.email}
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form(self):
        user = User.objects.create(first_name='reza', last_name='rezulu', username='Foo', password='bubu1234', email='')
        data = {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username, 'password': user.password, 'email': user.email}
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

class OfficeFormTest(TestCase):
    def test_valid_form(self):
        office = Office.objects.create(address='asdfasd', telephone='4123423')

        data = {'address': office.address, 'telephone': office.telephone}
        form = OfficeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        office = Office.objects.create(address='asdfasd', telephone='4123423')

        data = {'telephone': office.telephone, 'address1':'asfasdf09098'}
        form = OfficeForm(data=data)
        self.assertFalse(form.is_valid())

class VisitTimeIntervalFormTest(TestCase):
    def test_valid_form(self):

        data = {'startTime': '1:30', 'endTime': '1:40'}
        form = VisitTimeIntervalForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'address1': 'asfasdf09098'}
        form = VisitTimeIntervalForm(data=data)
        self.assertFalse(form.is_valid())

class InsuranceFormTest(TestCase):
    def test_valid_form(self):

        data = {'name': 'social'}
        form = Insurance(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'address': 'social'}
        form = Insurance(data=data)
        self.assertFalse(form.is_valid())