from django.shortcuts import render


def home(request):
    return render(request, 'directory/home.html')

def directory(request):
    return render(request, 'directory/directory.html')