from django import forms
from doctor.models import User, Doctor, DoctorDegree, Office, Insurance,VisitTimeInterval,DailyTimeTable
from django.contrib.admin.widgets import AdminDateWidget


class UserForm(forms.ModelForm):

    first_name = forms.CharField(label='نام')
    last_name = forms.CharField(label='نام خانوادگی')
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور')
    username = forms.CharField(label='نام کاربری')
    email = forms.CharField(label='پست الکترونیکی')

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name'}),
            'username': forms.TextInput(attrs={'id': 'usernamesignup'}),
            'email': forms.TextInput(attrs={'id': 'emailsignup'}),
            'password': forms.TextInput(attrs={'id': 'passwordsignup'}),
        }


class DoctorForm(forms.ModelForm):
    nationalID = forms.CharField(max_length=12,label='کد ملی')
    contractFile = forms.FileField(label='فایل قرارداد را انتخاب کنید')
    resume = forms.FileField(label='فایل رزومه را انتخاب کنید')
    picture = forms.ImageField(label='عکس پروفایل')

    class Meta:
        model = Doctor
        fields = ('nationalID','contractFile','resume','picture')
        widgets = {
            'nationalID': forms.TextInput(attrs={'id': 'nationalID'}),
            'contractFile': forms.TextInput(attrs={'id': 'contractFile'}),
            'resume': forms.TextInput(attrs={'id': 'resume'}),
            'picture': forms.TextInput(attrs={'id': 'picture'}),
        }

DOCTOR_DEGREE_CHOICES = (
    ('GL', 'عمومی'),
    ('MO', 'متخصص'),
    ('FT', 'فوق تخصص'),
    ('JR', 'جراح'),
)
DOCTOR_NAME_CHOICES = (
    ('aa', 'داخلی و غدد'),
    ('ab', 'عمومی'),
    ('ac', 'اورولوژی'),
    ('ad', 'زنان'),
    ('ae', 'گوارش'),
)

class DoctorDegreeForm(forms.ModelForm):
    # degree = forms.CharField(max_length=2,label='مدرک')
    degree = forms.ChoiceField(
        widget=forms.Select(attrs={'style': "width:442px;"}),
        choices=DOCTOR_DEGREE_CHOICES,
        required=True,
        label='مدرک'
    )
    # degreeTitle = forms.CharField(max_length=40,label='عنوان مدرک')
    degreeTitle = forms.ChoiceField(
        widget=forms.Select(attrs={'style': "float:right;width:442px;"}),
        choices=DOCTOR_NAME_CHOICES,
        required=True,
        label='عنوان مدرک'
    )
    university = forms.CharField(max_length=200,label='دانشگاه')
    endOfGraduate = forms.CharField(max_length=200,label='پایان تحصیل')

    class Meta:
        model = DoctorDegree
        fields = ('degree','university','endOfGraduate','degreeTitle')
        widgets = {
            'degree': forms.TextInput(attrs={'id':'degree'}),
            'university': forms.TextInput(attrs={'id': 'university'}),
            'endOfGraduate': forms.TextInput(attrs={'id': 'endOfGraduate'}),
            'degreeTitle': forms.TextInput(attrs={'id': 'degreeTitle'}),
        }


class OfficeForm(forms.ModelForm):
    address = forms.CharField(max_length=150,label='آدرس محل کار')
    telephone = forms.CharField(max_length=12,label='شماره محل کار')

    class Meta:
        model = Office
        fields = ('address','telephone',)
        widgets = {
            'address': forms.TextInput(attrs={'id':'address'}),
            'telephone': forms.TextInput(attrs={'id':'address'}),
        }

class Insurance(forms.ModelForm):
    name = forms.CharField(max_length=20)

    class Meta:
        model = Insurance
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'id':'name'}),
        }


class VisitTimeIntervalForm(forms.ModelForm):
    startTime = forms.CharField(label='ساعت شروع')
    endTime = forms.CharField(label='ساعت پایان')

    class Meta:
        model = VisitTimeInterval
        fields = ('startTime','endTime',)



class DailyTimeTableForm(forms.ModelForm):
    date = forms.DateField(label='تاریخ',widget=forms.TextInput(attrs={'id': 'datepicker'}))

    class Meta:
        model = DailyTimeTable
        fields = ('date',)


# class EditProfileForm(forms.Form):
#     email = forms.EmailField(required=True,label='پست الکترونیکی')
#     degreeTitle = forms.CharField(max_length=40,label='تخصص')
#     university = forms.CharField(max_length=200,label='دانشگاه محل تحصیل')
#     visitTime = forms.DecimalField(max_digits=2,decimal_places=2,label='مدت زمان ملاقات')



    # class Meta:
    #     model = DoctorDegree
    #     fields = ('degreeTitle', 'university',)
