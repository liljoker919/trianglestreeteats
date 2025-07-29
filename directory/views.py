from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib import messages
from .forms import WebsiteUserCreationForm


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
    """Website user registration view"""
    if request.method == 'POST':
        form = WebsiteUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            
            # Automatically log in the user after registration
            login(request, user)
            return redirect('profile')  # Redirect to profile page after successful registration
    else:
        form = WebsiteUserCreationForm()
    
    return render(request, 'registration/register_website_user.html', {'form': form})

def profile_view(request):
    """Placeholder profile view"""
    return render(request, 'registration/profile.html')