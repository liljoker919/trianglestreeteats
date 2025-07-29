from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect


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
    """Placeholder login view"""
    return render(request, 'registration/login.html')

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