from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings


def home(request):
    return render(request, 'directory/home.html')

def directory(request):
    return render(request, 'directory/directory.html')

def trucks_by_city(request, city):
    context = {'city': city}
    return render(request, 'directory/trucks_by_city.html', context)

def submit_truck(request):
    return render(request, 'directory/submit_truck.html')

# Authentication Views
def login_view(request):
    """Handle user login with form validation and authentication"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """Placeholder logout view"""
    logout(request)
    return redirect('home')

def register_view(request):
    """Placeholder register view"""
    return render(request, 'registration/register.html')

def profile_view(request):
    """Placeholder profile view"""
    return render(request, 'registration/profile.html')