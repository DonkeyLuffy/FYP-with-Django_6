import re
from django import forms
from user.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        'password2': forms.PasswordInput(attrs={'class': 'form-control', 'default':'kg'}),
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name',)
        widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileRegisteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

        widgets = {
            'user': forms.Select(attrs={'hidden':'true', 'required':'True'}),
            'adress': forms.TextInput(attrs={'class': 'form-control', 'required':'True'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control','placeholder':'yyyy-mm-dd' , 'required':'True'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required':'True'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'required':'True'}),
            'weight_type': forms.Select(attrs={'class': 'form-control ', 'required':'True'}),
            'shoe_size': forms.TextInput(attrs={'class': 'form-control', 'required':'True'}),
            'size_type': forms.Select(attrs={'class': 'form-control', 'required':'True'}),
        }

class DataBaseForm(forms.ModelForm):
    class Meta:
        model = DeviceData
        fields = '__all__'

        widgets = {
            'user': forms.Select(attrs={ 'required':'True'}),
            'heel': forms.NullBooleanSelect(attrs={'class': 'form-control',}),
            'bigtoe': forms.NullBooleanSelect(attrs={'class': 'form-control',}),
            'date': forms.DateInput(attrs={'class': 'form-control',}),
            'time': forms.TimeInput(attrs={'class': 'form-control',}),
        }
