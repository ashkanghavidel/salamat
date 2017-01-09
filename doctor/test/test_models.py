import datetime
from django.test import TestCase
from doctor.models import *
from django.contrib.auth.models import User
from django.utils import timezone




class DoctorTestCase(TestCase):
    def setUp(self):
        doctorDegree = DoctorDegree.objects.create(university='tehran2',endOfGraduate='1395',degree='GL',degreeTitle='beauty1')
        user = User.objects.create_user('john3', 'lennon@thebeatles.com', 'johnpassword', id=4)
        user.save()
        doctor = Doctor(user=user,doctorDegree=doctorDegree,id=3)
        doctor.save()
        return doctor

    def test_national_uniqueness(self):
        first = self.setUp()
        self.assertTrue(isinstance(first, Doctor))
        second = Doctor.objects.get(user=User.objects.get(username='john3'))
        self.assertEqual(first.doctorDegree.degree, second.doctorDegree.degree)

class DoctorDegreeTestCase(TestCase):
    def setUp(self):
        return DoctorDegree.objects.create(university='tehran',endOfGraduate='1394',degree='GL',degreeTitle='beauty')

    def test_national_uniqueness(self):
        first = self.setUp()
        self.assertTrue(isinstance(first, DoctorDegree))
        second = DoctorDegree.objects.filter(degree='GL')
        # self.assertEqual(len(DoctorDegree.objects.filter(degree='GL')), 1)
        self.assertEqual(second[0].university,first.university)


class OfficeTestCase(TestCase):
    def setUp(self):
        return Office.objects.create(address="No 33, Allame Jonubi",telephone='09128307749')

    def test_national_uniqueness(self):
        first = self.setUp()
        self.assertTrue(isinstance(first, Office))
        second = Office.objects.filter(address="No 33, Allame Jonubi",telephone='09128307749')
        self.assertEqual(first.__unicode__(), second[0].__unicode__())

class VisitTimeIntervalTestCase(TestCase):
    now = None
    end = None
    dailyTimeTable = None
    def setUp(self):
        doctorDegree = DoctorDegree.objects.create(university='tehran2', endOfGraduate='1395', degree='GL',
                                                   degreeTitle='beauty1')
        user = User.objects.create_user('john3', 'lennon@thebeatles.com', 'johnpassword', id=6)
        user.save()
        doctor = Doctor(user=user, doctorDegree=doctorDegree, id=6)
        doctor.save()
        dailyTimeTable = DailyTimeTable(doctor = doctor, date=datetime.date.today())
        dailyTimeTable.save()
        now = timezone.now()
        end = timezone.now()
        mylist = []
        mylist.append(now)
        mylist.append(end)
        mylist.append(VisitTimeInterval.objects.create(startTime= now, endTime= end, dailyTimeTable = dailyTimeTable))
        mylist.append(dailyTimeTable)
        return mylist

    def test_national_uniqueness(self):
        firstlist = self.setUp()
        self.assertTrue(isinstance(firstlist[2], VisitTimeInterval))
        second = VisitTimeInterval.objects.get(startTime=firstlist[0], endTime=firstlist[1], dailyTimeTable = firstlist[3])
        self.assertEqual(firstlist[2].__unicode__, second.__unicode__)

class InsuranceTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('john3', 'lennon@thebeatles.com', 'johnpassword', id=5)
        user.save()
        doctorDegree = DoctorDegree.objects.create(university='tehran2', endOfGraduate='1395', degree='GL',
                                                   degreeTitle='beauty1')
        doctor = Doctor(user = user, doctorDegree=doctorDegree, id=7)
        doctor.save()
        mylist = []
        mylist.append(doctor)
        mylist.append(Insurance.objects.create(name='social1', doctor=doctor))
        return mylist

    def test_national_uniqueness(self):
        firstlist = self.setUp()
        print(self.assertTrue(isinstance(firstlist[1], Insurance)))
        second = Insurance.objects.filter(name='social1').filter(doctor=firstlist[0])
        self.assertEqual(firstlist[1].__unicode__, second[1].__unicode__)



