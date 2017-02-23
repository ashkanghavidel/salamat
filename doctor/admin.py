from django.contrib import admin
from doctor.models import *

admin.site.register(DoctorDegree)
admin.site.register(Office)
admin.site.register(Doctor)
admin.site.register(Insurance)
admin.site.register(DailyTimeTable)
admin.site.register(VisitTimeInterval)
admin.site.register(VisitTimeIntervalMap)
admin.site.register(VisitPayment)
admin.site.register(PatientComment)
admin.site.register(PatientRate)


