from django.contrib import admin
from doctor.models import *

admin.site.register(DoctorDegree)
admin.site.register(Office)
admin.site.register(Doctor)
admin.site.register(Insurance)
admin.site.register(DailyTimeTable)
admin.site.register(VisitTimeInterval)

