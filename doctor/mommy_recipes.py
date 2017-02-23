import datetime
from model_mommy.recipe import Recipe, foreign_key

from doctor.models import *
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

user = Recipe(
    User,
    username = 'john3',
    email = 'lennon@thebeatles.com',
    first_name = 'reza',
    last_name = 'khazali',
    password = 'johnpassword'
)

doctorDegree = Recipe(
    DoctorDegree,
    university='tehran2',
    endOfGraduate='1395',
    degree='GL',
    degreeTitle='beauty1',
)

doctor = Recipe(
    Doctor,
    user = foreign_key(user),
    doctorDegree = foreign_key(doctorDegree),
)

insurance = Recipe(
    Insurance,
    doctor = foreign_key(doctor),
    name = 'my_social_insurance'
)

office = Recipe(
    Office,
    address =  'faffa',
    telephone = '091230948123',
)