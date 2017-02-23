import datetime
from doctor.models import *
from django.test import TestCase



class DoctorTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        mydoctor = Doctor.objects.filter(pk=1).first()
        self.assertEqual(mydoctor.nationalID, "1234")
        self.assertTrue(isinstance(mydoctor, Doctor))


class DoctorDegreeTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        mydoctordegree = DoctorDegree.objects.filter(pk=1).first()
        self.assertEqual(mydoctordegree.university, "sharif")
        self.assertTrue(isinstance(mydoctordegree, DoctorDegree))

    def field_test(self):
        mydoctordegree = DoctorDegree.objects.get(id=1)
        field_label = mydoctordegree._meta.get_field(
            'university').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'university')  # Compare the value to the expected result


class OfficeTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        myoffice = Office.objects.filter(pk=3).first()
        self.assertEqual(myoffice.address, "sadeghie")
        self.assertTrue(isinstance(myoffice, Office))

    def field_test(self):
        myoffice = Office.objects.get(id=1)
        field_label = myoffice._meta.get_field(
            'address').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'address')  # Compare the value to the expected result

class VisitTimeIntervalTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        myvisittimeinterval = VisitTimeInterval.objects.filter(pk=1).first()
        self.assertEqual(myvisittimeinterval.startTime, datetime.time(0,0))
        self.assertEqual(myvisittimeinterval.endTime, datetime.time(7,12,2))
        self.assertTrue(isinstance(myvisittimeinterval, VisitTimeInterval))

    def field_test(self):
        myvisittimeinterval = VisitTimeInterval.objects.get(id=1)
        field_label = myvisittimeinterval._meta.get_field(
            'startTime').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'startTime')  # Compare the value to the expected result

class VisitTimeIntervalMapTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        myvisittimeintervalmap = VisitTimeIntervalMap.objects.filter(pk=1).first()
        self.assertEqual(myvisittimeintervalmap.doctor.user.username, 'rk')
        self.assertEqual(myvisittimeintervalmap.doctor.user.first_name, 'mohsen')
        self.assertTrue(isinstance(myvisittimeintervalmap, VisitTimeIntervalMap))

    def field_test(self):
        myvisittimeintervalmap = VisitTimeIntervalMap.objects.get(id=1)
        field_label = myvisittimeintervalmap._meta.get_field(
            'checked').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'checked')  # Compare the value to the expected result

class VisitPaymentTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        myvisitpayment = VisitPayment.objects.filter(pk=1).first()
        self.assertEqual(myvisitpayment.cashAmount, 12342314.0)
        self.assertEqual(myvisitpayment.status, True)
        self.assertTrue(isinstance(myvisitpayment, VisitPayment))

    def field_test(self):
        myvisitpayment = VisitPayment.objects.get(id=1)
        field_label = myvisitpayment._meta.get_field(
            'cashAmount').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'cashAmount')  # Compare the value to the expected result

class InsuranceTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        myinsurance = Insurance.objects.filter(pk=3).first()
        self.assertEqual(myinsurance.name, 'bime_alavi')
        self.assertTrue(isinstance(myinsurance, Insurance))

    def field_test(self):
        myinsurance = Insurance.objects.get(id=1)
        field_label = myinsurance._meta.get_field(
            'name').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'name')  # Compare the value to the expected result
