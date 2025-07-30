from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib import messages
from .forms import FoodTruckOwnerRegistrationForm


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

def register_food_truck_owner(request):
    """Registration view for food truck owners"""
    if request.method == 'POST':
        form = FoodTruckOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Triangle Street Eats.')
            return redirect('profile')
    else:
        form = FoodTruckOwnerRegistrationForm()
    
    return render(request, 'registration/register_food_truck_owner.html', {'form': form})