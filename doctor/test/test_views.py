import datetime
import unittest
from mock.mock import patch
from freezegun import freeze_time
from doctor.forms import *
from doctor.views import *
from model_mommy import mommy
from django.test import Client
from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from model_mommy.recipe import Recipe, foreign_key
from django.contrib.auth import authenticate



class TestCalls(TestCase):
    def setUp(self):
        self.user = User()
        self.user.username = 'user'
        self.user.password = 'test'
    def test_call_view_denies_anonymous(self):
        response = self.client.get('/doctor/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/doctor/register/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/doctor/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/register-login.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/doctor/register', {}) # blank data dictionary



class user_loginTest(TestCase):
    def setUp(self):
        self.user = User(username='salam', password='salam1', email='salam1@salam.com')
    def tearDown(self):
        del self.user

    def test_login(self):
        user1 = authenticate(username='salam', password='salam1')
        user2 = authenticate(username=self.user.username, password = self.user.password)


class login_Test_Case(TestCase):
    fixtures = ['info.json']
    def test_post(self):
        client = Client()
        response = client.post('/doctor/login/', {'username': 'rk', 'password': 'hello1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'main_Side/index.html')


class search_Test(TestCase):
    fixtures = ['info.json']
    def test_post(self):
        c = Client()
        response = c.post('/doctor/search/', {'degree-title': 'MO', 'office-address': 'sharif', 'insurance':'faffa'})
        # mydoctors = Doctor.objects.filter(user=User.objects.get(username='rk'))
        # print(mydoctors[0].doctorDegree.university)
        # self.assertEqual(list(response.context)[0]['doctors'], mydoctors)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/search.html')


class account_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]
    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.get('/doctor/account/',
                                   {'user': self.user})
        doctor = Doctor.objects.get(user=self.user)
        self.assertEqual(list(response.context)[0]['doctor'], doctor)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/account.html')
class account_addtime_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        data_table = {'date': '02/04/2017'}
        daily_time_table_form = DailyTimeTableForm(data=data_table)
        data_interval = {'startTime': '10:20', 'endTime': '10:40'}
        visit_time_interval_form = VisitTimeIntervalForm(data=data_interval)
        response = self.client.get('/doctor/account/add-time/',
                                   {'user': self.user,'daily_time_table_form':daily_time_table_form,
                                                        'visit_time_interval_form':visit_time_interval_form})
        self.assertEqual(response.status_code, 302)

class account_edit_information_Test(TestCase):
    fixtures = ['info.json']

    def setUp(self):
        users = User.objects.filter(username='test_user1')
        self.user = users[0]

    def tearDown(self):
        del self.user
    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.post('/doctor/account/edit-information/',
                          {'user':self.user, 'degreeTitle': 'GL', 'university': 'amirkabir', 'email': 'reza@gmail.com', 'visitDuration': '2'})
        self.assertEqual(Doctor.objects.get(user=self.user).doctorDegree.university,'amirkabir')
        self.assertEqual(response.status_code, 302)

class account_complete_information(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        mydoctor_office = Doctor.objects.get(user=self.user).office.address
        print(mydoctor_office)
        response = self.client.post('/doctor/account/complete-information/',{
            'user': self.user, 'address': 'bugu', 'telephone': '88692165', 'removed-insurance': 'salam',
                           })
        mydoctor_office = Doctor.objects.get(user=self.user).office.address
        self.assertEqual(mydoctor_office,'bugu')
        self.assertEqual(response.status_code, 302)

class reserve_visit_time(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        mydoctor_office = Doctor.objects.get(user=self.user).office.address
        print(mydoctor_office)
        response = self.client.post('/doctor/reserve-visit-time/', {
            'user': self.user
        })
        # mydoctor_office = Doctor.objects.get(user=self.user).office.address
        # self.assertEqual(mydoctor_office, 'bugu')
        self.assertEqual(response.status_code, 200)

class get_week_range_Test(TestCase):
    def setUp(self):
        self.this_time = datetime.datetime.now()
        self.time_list = get_week_range(self.this_time)

    def tearDown(self):
        del self.this_time
        del self.time_list

    def test_times(self):
        time_list = get_week_range(self.this_time)
        self.assertEqual(self.time_list,
                         time_list)

class account_time_table_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_get(self):
        user = self.client.force_login(self.user)
        response = self.client.post('/doctor/account/time-table/rk',
                          {'user': self.user,'doctor_user_name':'rk'})
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'doctor/time-table.html')
class get_accepted_visit_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_get(self):
        user = self.client.force_login(self.user)
        response = self.client.post('/doctor/account/show-accepted-visit/',
                          {'user': self.user})
        self.assertEqual(list(response.context)[0]['visit_time_interval_maps'][0].doctor.user.username,'rk')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/accepted-visit.html')

class get_paid_visit_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_get(self):
        user = self.client.force_login(self.user)
        response = self.client.post('/doctor/account/show-paid-visit/',
                          {'user': self.user})
        print(list(response.context)[0])
        self.assertEqual(list(response.context)[0]['visits_paid'][0].visitTimeIntervalMap.doctor.user.username,'rk')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/paid-visit.html')


class get_pending_visit_time_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    @freeze_time("2017-01-21")
    def test_get(self):
        freezer = freeze_time("2017-01-21 12:00:01")
        freezer.start()
        assert datetime.datetime.now() == datetime.datetime(2017, 1, 21, 12, 0, 1)
        user = self.client.force_login(self.user)
        response = self.client.get('/doctor/account/show-pending/',
                         {'user': user})
        week_range = get_week_range(datetime.date.today())
        first_day_of_week = week_range[0]
        last_day_of_week = week_range[1]
        doctor = Doctor.objects.get(user=self.user)
        visit_time_interval_maps = VisitTimeIntervalMap.objects.filter(
            visitTimeInterval__dailyTimeTable__date__range=[first_day_of_week, last_day_of_week],
            doctor=doctor, status=False, checked=False)
        # self.assertEqual(list(response.context)[0]['visit_time_interval_maps'][0],visit_time_interval_maps[0])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/pending-request.html')
        freezer.stop()


class profile_interface_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        self.client = Client()
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.client
        del self.user
    def test_get(self):
        user = self.client.force_login(self.user)
        response = self.client.get('/doctor/profile-interface/rk/',
                         {'user': self.user,'doctor_user_name':'rk'})
        doctor = Doctor.objects.get(user=self.user)
        self.assertEqual(list(response.context)[0]['doctor'],doctor)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/profile-interface.html')

class account_time_table_for_patientTest(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        self.client = Client()
        users = User.objects.filter(username='rk')
        self.user = users[0]
    def tearDown(self):
        del self.user
        del self.client
    def test_get(self):
        user = self.client.force_login(self.user)
        response = self.client.get('/doctor/account/time-table/rk',
                         {'user': self.user,'doctor_user_name':'rk'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context)[0]['next_week_first_day'], datetime.date(2017, 2, 25))
        self.assertTemplateUsed(response, 'doctor/time-table.html')



class next_or_previous_account_time_tableTest(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        self.client = Client()
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.client
        del self.user
    def test_post(self):
        user = self.client.force_login(self.user)
        this_date = datetime.date(2017,2,3)
        response = self.client.post('/doctor/time-table/rk/2017-Feb-03',
                         {'user': user,'doctorUserName':'rk','next_or_previous_date':this_date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context)[0]['previous_week_first_day'],datetime.datetime(2017, 1, 21, 0, 0))
        self.assertEqual(list(response.context)[0]['next_week_first_day'],datetime.datetime(2017, 2, 4, 0, 0))
        self.assertTemplateUsed(response, 'doctor/time-table.html')

class Get_paid_visit_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user

    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.get('/doctor/account/show-paid-visit/',
                         {'user': self.user})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/paid-visit.html')


class Get_accepted_visit_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]

    def tearDown(self):
        del self.user
        pass

    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.get('/doctor/account/show-accepted-visit/',
                                              {'user': user})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/accepted-visit.html')

class set_job_status_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        self.visit_time_interval_map = VisitTimeIntervalMap.objects.filter(isDone=True).first()

    def tearDown(self):
        del self.visit_time_interval_map

    def test_post(self):
        users = User.objects.filter(username='rk')
        user = self.client.force_login(users.first())
        response = self.client.post('/doctor/account/job-status/done',
                                              {'visit-map-id': 1,'cash-amount':'3500','responseType':'done'})
        self.assertEqual(response.status_code, 302)


class account_accept_or_reject_request_Test(TestCase):
    fixtures = ['info.json']
    def setUp(self):
        users = User.objects.filter(username='rk')
        self.user = users[0]
    def tearDown(self):
        del self.user

    def test_info(self):
        d = Doctor.objects.filter(pk = 1).first()
        self.assertEqual(d.nationalID, "1234")

    def test_post(self):
        user = self.client.force_login(self.user)
        response = self.client.post('/doctor/account/accept-reject-request/salam',
                                              {'visit-map-id':1})
        myvisittimeintervalmap = VisitTimeIntervalMap.objects.get(pk=1)
        self.assertEqual(myvisittimeintervalmap.status,True)
        print (response)
        self.assertEqual(response.status_code, 302)

    @freeze_time("2012-01-14")
    def test_first_and_last_day_of_the_week(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        assert datetime.datetime.now() == datetime.datetime(2012, 1, 14, 12, 0, 1)
        user = self.client.force_login(self.user)
        response = self.client.post('/doctor/account/time-table/rk',
                                    {'user': user, 'doctorUserName': 'rk'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context)[0]['previous_week_first_day'], datetime.date(2012, 1, 7))
        self.assertEqual(list(response.context)[0]['next_week_first_day'], datetime.date(2012, 1, 21))
        self.assertTemplateUsed(response, 'doctor/time-table.html')
        freezer.stop()


    def datetime_now_mock(self):
        assert datetime.datetime.now() != datetime.datetime(2012, 1, 14)
        with freeze_time("2012-01-14"):
            assert datetime.datetime.now() == datetime.datetime(2012, 1, 14)
        assert datetime.datetime.now() != datetime.datetime(2012, 1, 14)

    @freeze_time("2012-01-14")
    def test_90(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        assert datetime.datetime.now() == datetime.datetime(2012, 1, 14, 12, 0, 1)
        freezer.stop()

