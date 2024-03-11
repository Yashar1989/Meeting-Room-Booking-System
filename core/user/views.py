from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages

from .models import Profile
from .forms import CustomUserCreationForm, CustonUserLoginForm, CustomUserEditForm

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
    pass