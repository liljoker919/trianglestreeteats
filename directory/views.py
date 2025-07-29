from django.shortcuts import render


def home(request):
    return render(request, 'directory/home.html')

def directory(request):
    return render(request, 'directory/directory.html')

def trucks_by_city(request, city):
    context = {'city': city}
    return render(request, 'directory/trucks_by_city.html', context)

def submit_truck(request):
    return render(request, 'directory/submit_truck.html')