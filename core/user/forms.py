from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.validators import EmailValidator

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام کاربری'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ایمیل'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'شماره موبایل'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})

        for _, field in self.fields.items():
            field.label = ''

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")
        error_messages = {
            'name': {
                'max_length': ("This writer's name is too long."),
            },
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ایمیل'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})

        for _, field in self.fields.items():
            field.label = ''

    class Meta:
        fields = ("username", "password")


class CustomUserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='نام', required=False)
    last_name = forms.CharField(label='نام خانوادگی', required=False)
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


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'روز قدیم', 'class': 'form-control'}))
    new_password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'رمز جدید', 'class': 'form-control'}))
    new_password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز جدید', 'class': 'form-control'}))

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class EmailCheckForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'ایمیل', 'class': 'form-control'}), validators=[EmailValidator])


class OTPLoginForm(forms.Form):
    otp = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'کد یک بار مصرف', 'class': 'form-control'}))
