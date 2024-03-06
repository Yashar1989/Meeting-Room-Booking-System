from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2") 

class CustonUserLoginForm(forms.Form):
    username = forms.CharField(label='Phone number or email')
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='first name')
    last_name = forms.CharField(label='last name')
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'description', 'image']

    def clean(self):
        cd = super().clean()
        
        profile = Profile.objects.get(user=self.instance.id)
        profile.first_name = cd['first_name']
        profile.last_name = cd['last_name']
        profile.description = cd['description']
        print(cd)
        profile.save()

        return cd
        

