from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2") 

class CustonUserLoginForm(forms.Form):
    username = forms.CharField(label='Phone number or email')
    password = forms.CharField(widget=forms.PasswordInput)