from django.test import TestCase
from patient.models import Patient
from django.contrib.auth.models import User

class PatientTestCase(TestCase):
    fixtures = ['info.json']
    def test_national_uniqueness(self):
        mypatient = Patient.objects.filter(pk=1).first()
        self.assertEqual(mypatient.nationalId, "12341234")
        self.assertEqual(mypatient.phoneNumber, "123412342")
        self.assertTrue(isinstance(mypatient, Patient))

    def field_test(self):
        mypatient = Patient.objects.get(id=1)
        field_label = mypatient._meta.get_field(
            'nationalId').verbose_name  # Get the metadata for the required field and use it to query the required field data
        self.assertEquals(field_label, 'nationalId')  # Compare the value to the expected result