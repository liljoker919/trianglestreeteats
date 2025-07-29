from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser to support
    three distinct user types: Food Truck Owner, Admin, and Website User.
    """
    
    USER_ROLES = [
        ('food_truck_owner', 'Food Truck Owner'),
        ('admin', 'Admin'),
        ('website_user', 'Website User'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='website_user',
        help_text='User role type'
    )
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Phone number for contact'
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        help_text='User address'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class FoodTruckOwnerProfile(models.Model):
    """
    Profile model for Food Truck Owners with additional specific information.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='food_truck_profile'
    )
    
    business_name = models.CharField(
        max_length=100,
        help_text='Name of the food truck business'
    )
    
    business_license = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Business license number'
    )
    
    cuisine_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Type of cuisine served'
    )
    
    operating_hours = models.TextField(
        blank=True,
        null=True,
        help_text='Operating hours and schedule'
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the food truck is verified by admin'
    )
    
    def __str__(self):
        return f"{self.business_name} - {self.user.username}"


class WebsiteUserProfile(models.Model):
    """
    Profile model for Website Users with additional preferences.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='website_user_profile'
    )
    
    dietary_preferences = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Dietary preferences (vegetarian, vegan, etc.)'
    )
    
    favorite_cuisine_types = models.TextField(
        blank=True,
        null=True,
        help_text='Favorite types of cuisine'
    )
    
    notification_preferences = models.BooleanField(
        default=True,
        help_text='Whether to receive notifications about new food trucks'
    )
    
    def __str__(self):
        return f"Profile for {self.user.username}"
