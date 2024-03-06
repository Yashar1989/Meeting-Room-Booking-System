from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages

from .models import Profile
from .forms import CustomUserCreationForm, CustonUserLoginForm, CustomUserEditForm

User = get_user_model()

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form' : form})

def login_user(request):
    if request.method == "POST":
        form = CustonUserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('account:profile')
            messages.error(request, "No account found")
            return render(request, 'user/login.html', {'form':form})
    else:
        form = CustonUserLoginForm()
    return render(request, 'user/login.html', {'form':form})

def profile(request):
    return HttpResponse("Profile page")

def edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(User, id=request.user.id)
    form = CustomUserEditForm(instance=user)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('account:profile'))
    return render(request, 'user/register.html', {'form' : form})

def change_password(request):
    pass