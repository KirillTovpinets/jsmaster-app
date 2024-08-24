from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, UpdateUserForm, ProfileForm
from . models import Profile
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login as authLogin, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'app_auth/index.html')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)

            form.save()

            send_mail("Welcome to EdenThought", "Thank you for signing up with EdenThought", settings.DEFAULT_FROM_EMAIL, [current_user.email], fail_silently=False)
            Profile.objects.create(user=current_user)
            messages.success(request, 'Account created successfully')
            return redirect('login')

    context = {'RegistrationForm': form}

    return render(request, 'app_auth/register.html', context)


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            authLogin(request, user)
            return redirect('dashboard')

    context = {'LoginForm': form}
    return render(request, 'app_auth/login.html', context)

@login_required(login_url='login')
def profile(request):
    form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.get(user=request.user)

    form_2 = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        form_2 = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

        if form_2.is_valid():
            form_2.save()
            return redirect('dashboard')

    context = {'UserUpdateForm': form, 'ProfileForm': form_2}
    return render(request, 'app_auth/profile.html', context)
