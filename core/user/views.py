from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

from .utils import generate_number
from .models import Profile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserEditForm, CustomPasswordChangeForm, EmailCheckForm, OTPLoginForm

User = get_user_model()

def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('account:profile'))
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.

@guest_required
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('account:login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form' : form, 'title' : 'Register new user'})

@guest_required
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect(reverse_lazy('account:profile'))
            messages.error(request, "No account found")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'user/login.html', {'form': form})

@guest_required
def send_otp(request):
    if request.method == 'POST':
        form = EmailCheckForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                otp = generate_number()
                user.stored_otp = otp
                print(otp)
                user.save()
                request.session['email'] = user.email
                return redirect(reverse_lazy('account:verify_otp'))
            except:
                messages.error(request, 'Email not found !!!')
    form = EmailCheckForm()
    return render(request, 'user/otp.html', {'form' : form, 'title' : 'send otp'})
        
@guest_required
def verify_otp(request):
    if request.method == 'POST':
        form = OTPLoginForm(request.POST)
        if form.is_valid():
            stored_email = request.session.get('email')
            user = User.objects.get(email=stored_email)
            given_otp = form.cleaned_data['otp']
            user = authenticate(request, username=stored_email, password=given_otp)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect(reverse_lazy('account:profile'))
            messages.error(request, 'Incorrect OTP')
    form = OTPLoginForm()
    return render(request, 'user/otp.html', {'form':form, 'title': 'login'})

@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=request.user)
    print(profile.image)
    return render(request, 'user/profile.html', {'user' : user, 'profile' : profile})

@login_required
def edit(request):
    user = get_object_or_404(User, id=request.user.id)
    form = CustomUserEditForm(instance=user)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('account:profile'))
    return render(request, 'user/register.html', {'form' : form, 'title' : "Edit user data"})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('account:profile'))
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user/register.html', {'form': form, 'title' : 'Change Password'})

@login_required
def logout_view(request):
    logout(request)
    return redirect('room:index')