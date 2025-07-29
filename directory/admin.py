from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FoodTruckOwnerProfile, WebsiteUserProfile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser model.
    """
    # Add the custom fields to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'address'),
        }),
    )
    
    # Add fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'address'),
        }),
    )
    
    # Display these fields in the user list
    list_display = UserAdmin.list_display + ('role', 'phone_number')
    list_filter = UserAdmin.list_filter + ('role',)


class FoodTruckOwnerProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for FoodTruckOwnerProfile model.
    """
    list_display = ('business_name', 'user', 'cuisine_type', 'is_verified')
    list_filter = ('is_verified', 'cuisine_type')
    search_fields = ('business_name', 'user__username', 'business_license')
    readonly_fields = ('user',)


class WebsiteUserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for WebsiteUserProfile model.
    """
    list_display = ('user', 'dietary_preferences', 'notification_preferences')
    list_filter = ('notification_preferences',)
    search_fields = ('user__username', 'dietary_preferences')
    readonly_fields = ('user',)


# Register the models with their admin configurations
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FoodTruckOwnerProfile, FoodTruckOwnerProfileAdmin)
admin.site.register(WebsiteUserProfile, WebsiteUserProfileAdmin)
