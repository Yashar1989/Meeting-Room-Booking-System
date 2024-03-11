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
    first_name = forms.CharField(label='first name', required=False)
    last_name = forms.CharField(label='last name', required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                profile = self.instance.profile
                self.initial['first_name'] = profile.first_name
                self.initial['last_name'] = profile.last_name
                self.initial['description'] = profile.description
                self.initial['image'] = profile.image
            except Profile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super(CustomUserEditForm, self).save(commit=False)
        user.save()
        # print(type(user))
        if commit:
            try:
                profile = Profile.objects.get(user=user)
                profile.first_name = self.cleaned_data['first_name']
                profile.last_name = self.cleaned_data['last_name']
                profile.description = self.cleaned_data['description']
                if 'image' in self.cleaned_data:
                    profile.image = self.cleaned_data['image']
                profile.save()
            except Profile.DoesNotExist:
                Profile.objects.create(user=user, first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], description=self.cleaned_data['description'], image=self.cleaned_data['image'])
        
        return user