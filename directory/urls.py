from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('directory/', views.directory, name='directory'),
    path('trucks/<str:city>/', views.trucks_by_city, name='trucks_by_city'),
    path('submit/', views.submit_truck, name='submit_truck'),
]
