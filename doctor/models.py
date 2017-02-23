from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

DATE_INPUT_FORMATS = '%d-%m-%Y'


class Office(models.Model):
    address = models.CharField(max_length=150)
    telephone = models.CharField(max_length=12)

    def __str__(self):
        return "%s - %s" % (self.address,self.telephone)

DOCTOR_NAME_CHOICES = (
    ('aa', 'داخلی و غدد'),
    ('ab', 'عمومی'),
    ('ac', 'اورولوژی'),
    ('ad', 'زنان'),
    ('ae', 'گوارش'),
)

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
    degreeTitle = models.CharField(max_length=2, choices=DOCTOR_NAME_CHOICES, default='aa')

    def __str__(self):
        return "%s - %s" % (self.university,self.endOfGraduate)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.OneToOneField(Office,null=True)
    nationalID = models.CharField(max_length=10,unique=True)
    doctorDegree = models.OneToOneField(DoctorDegree)
    visitDuration = models.IntegerField(default=1,null=True)
    contractFile = models.FileField(upload_to='media/user_contract',null=True)
    resume = models.FileField(upload_to='media/user_resume',null=True)
    picture = models.ImageField(upload_to='media/user_picture',null=True)

    def __str__(self):
        return self.user.username


class DailyTimeTable(models.Model):
    date = models.DateField()
    doctor = models.ForeignKey(Doctor)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return "%s - %s" % (self.date,self.doctor.nationalID)


class VisitTimeInterval(models.Model):
    startTime = models.TimeField()
    endTime = models.TimeField()
    dailyTimeTable = models.ForeignKey(DailyTimeTable, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.startTime,self.endTime)


class Insurance(models.Model):
    name = models.CharField(max_length=20)
    doctor = models.ForeignKey(Doctor)

    def __str__(self):
        return "%s - %s" % (self.name,self.doctor.nationalID)


class VisitTimeIntervalMap(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    visitTimeInterval = models.OneToOneField(VisitTimeInterval, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    isDone = models.BooleanField(default=False)


class VisitPayment(models.Model):
    visitTimeIntervalMap = models.OneToOneField(VisitTimeIntervalMap, on_delete=models.CASCADE)
    cashAmount = models.FloatField(default=0)
    status = models.BooleanField(default=False)


class PatientComment(models.Model):
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    text = models.TextField()


class PatientRate(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    lastRate = models.IntegerField(default=0)
    totalRate = models.IntegerField(default=0)

# class PatientRate(models.Model):
#     doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
#     rate = models.IntegerField(default=0)
#     __totalRate = models.IntegerField(db_column='totalRate',default=0)
#
#     @property
#     def totalRate(self):
#         return (self.qty + self.totalRate)/self.numOfrate
#     numOfrate = models.IntegerField(default=0)
