from django import forms
from patient.models import User,Patient


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='رمز عبور')
    first_name = forms.CharField(label='نام')
    last_name = forms.CharField(label='نام خانوادگی')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name'}),
            'password': forms.TextInput(attrs={'id': 'passwordsignup'}),
        }


class PatientForm(forms.ModelForm):
    nationalId = forms.CharField(label='کد ملی')
    phoneNumber = forms.CharField(label='شماره تلفن')
    # picture = forms.ImageField(label='عکس پروفایل')

    class Meta:
        model = Patient
        fields = ('nationalId', 'phoneNumber',)
        widgets = {
            "nationalId": forms.TextInput(attrs={'id': 'national_id'}),
            "phoneNumber": forms.TextInput(attrs={'id': 'phone_number'}),
            # 'picture': forms.TextInput(attrs={'id': 'picture'}),
        }