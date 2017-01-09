from django.test import TestCase
from patient.models import Patient
from django.contrib.auth.models import User

class PatientTestCase(TestCase):
    def setUp(self):
        Patient.objects.create(user=User.objects.create_user(username='hr1'), nationalId='112', phoneNumber='134')

    def test_national_uniqueness(self):
        first = Patient.objects.get(user=User.objects.get(username='hr1'))
        self.assertTrue(isinstance(first, Patient))
        self.assertEqual(first.phoneNumber, '134')