from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('directory/', views.directory, name='directory'),
    path('trucks/<str:city>/', views.trucks_by_city, name='trucks_by_city'),
    path('submit/', views.submit_truck, name='submit_truck'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/food-truck-owner/', views.register_food_truck_owner, name='register_food_truck_owner'),
    path('profile/', views.profile_view, name='profile'),
]
