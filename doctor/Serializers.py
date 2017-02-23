from rest_framework import serializers
from doctor.models import *
from datetime import datetime
from pytz import timezone, utc
import pytz
from django.utils.timesince import timesince
from rest_framework.serializers import (
    ModelSerializer,
    ListSerializer,
    Serializer,

)
from django.contrib.auth.models import User

# from rest_framework import serializers
# from doctor.models import VisitTimeInterval
#
#
# class CreateVisitTimeIntervalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VisitTimeInterval
#         fields = ('startTime', 'endTime')
#


class DailyTimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyTimeTable
        fields = ('date', 'doctor')



class VisitTimeIntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitTimeInterval
        fields = ('startTime', 'endTime', 'status')

