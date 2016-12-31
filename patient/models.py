from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nationalId = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=200)

    def __unicode__(self):
        return self.user.username

