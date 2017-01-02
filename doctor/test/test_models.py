from django.test import TestCase
from doctor.models import Doctor,DoctorDegree
from django.contrib.auth.models import User


class DoctorTestCase(TestCase):
    def setUp(self):
        doctorDegree = DoctorDegree.objects.create(university='tehran',endOfGraduate='1394',degree='GL',degreeTitle='beauty')
        Doctor.objects.create(user=User.objects.create_user(username='hr1'),doctorDegree=doctorDegree)

    def test_national_uniqueness(self):
        first = Doctor.objects.get(user=User.objects.get(username='hr1'))
        self.assertEqual(first.doctorDegree.degree, 'GL')

class DoctorDegreeTestCase(TestCase):
    def setUp(self):
        DoctorDegree.objects.create(university='tehran',endOfGraduate='1394',degree='GL',degreeTitle='beauty')

    def test_national_uniqueness(self):
        first = DoctorDegree.objects.get(degree='GL')
        self.assertEqual(len(DoctorDegree.objects.filter(degree='GL')), 1)
        self.assertEqual(first.university,'tehran')
