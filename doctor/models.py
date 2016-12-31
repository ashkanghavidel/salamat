from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime
# from django.utils import timezone

DATE_INPUT_FORMATS = '%d-%m-%Y'


class Office(models.Model):
    address = models.CharField(max_length=150)
    telephone = models.CharField(max_length=12)

    def __unicode__(self):
        return "%s - %s" % (self.address,self.telephone)


class DoctorDegree(models.Model):
    university = models.CharField(max_length=200)
    endOfGraduate = models.CharField(max_length=200)
    DOCTOR_DEGREE_CHOICES = (
        ('GL', 'عمومی'),
        ('MO', 'متخصص'),
        ('FT', 'فوق تخصص'),
        ('JR', 'جراح'),
    )
    degree = models.CharField(max_length=2, choices=DOCTOR_DEGREE_CHOICES, default='GL')
    degreeTitle = models.CharField(max_length=40)

    def __unicode__(self):
        return "%s - %s" % (self.university,self.endOfGraduate)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.OneToOneField(Office,null=True)
    nationalID = models.CharField(max_length=10,unique=True)
    doctorDegree = models.OneToOneField(DoctorDegree)
    visitDuration = models.IntegerField(null=True)
    contractFile = models.FileField(upload_to='media/user_contract',null=True)
    resume = models.FileField(upload_to='media/user_resume',null=True)
    picture = models.ImageField(upload_to='media/user_picture',null=True)

    def __unicode__(self):
        return self.user.username


# class Document(models.Model):
#     contractFile = models.FileField(upload_to='media/user_contract')

class DailyTimeTable(models.Model):
    date = models.DateField()
    doctor = models.ForeignKey(Doctor)

    def __unicode__(self):
        return "%s - %s" % (self.date,self.doctor.nationalID)


class VisitTimeInterval(models.Model):
    startTime = models.TimeField()
    endTime = models.TimeField()
    dailyTimeTable = models.ForeignKey(DailyTimeTable, on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s - %s" % (self.startTime,self.endTime)


class Insurance(models.Model):
    name = models.CharField(max_length=20)
    doctor = models.ForeignKey(Doctor)

    def __unicode__(self):
        return "%s - %s" % (self.name,self.doctor.nationalID)

# class WorkingSchedule(models.Model):
#     title = models.CharField(max_length=50,null=True)
#     doctor = models.ForeignKey('doctor.models.Doctor', on_delete=models.CASCADE)
#     patient = models.ForeignKey('patient.Patient',on_delete=models.CASCADE,null=True)
#     visit_date = models.DateField(null=True)
#     start_hour = models.CharField(max_length=50)
#     end_hour = models.CharField(max_length=50)

