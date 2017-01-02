from rest_framework import serializers
from doctor.models import VisitTimeInterval


class CreateVisitTimeIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitTimeInterval
        fields = ('startTime', 'endTime')

