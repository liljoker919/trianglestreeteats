from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser, FoodTruckOwnerProfile, WebsiteUserProfile

# Create your tests here.

User = get_user_model()


class CustomUserModelTest(TestCase):
    """
    Test cases for the CustomUser model.
    """
    
    def test_create_user_default_role(self):
        """Test creating a user with default role."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.role, 'website_user')
        self.assertEqual(str(user), 'testuser (Website User)')
    
    def test_create_food_truck_owner(self):
        """Test creating a food truck owner user."""
        user = User.objects.create_user(
            username='truckowner',
            email='owner@truck.com',
            password='truckpass123',
            role='food_truck_owner',
            phone_number='555-0123',
            address='123 Main St'
        )
        self.assertEqual(user.role, 'food_truck_owner')
        self.assertEqual(user.phone_number, '555-0123')
        self.assertEqual(user.address, '123 Main St')
        self.assertEqual(str(user), 'truckowner (Food Truck Owner)')
    
    def test_create_admin_user(self):
        """Test creating an admin user."""
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.assertEqual(user.role, 'admin')
        self.assertEqual(str(user), 'admin (Admin)')
    
    def test_user_role_choices(self):
        """Test that user roles are properly constrained."""
        valid_roles = ['food_truck_owner', 'admin', 'website_user']
        for role_value, role_display in User.USER_ROLES:
            self.assertIn(role_value, valid_roles)


class FoodTruckOwnerProfileTest(TestCase):
    """
    Test cases for the FoodTruckOwnerProfile model.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='truckowner',
            email='owner@truck.com',
            password='truckpass123',
            role='food_truck_owner'
        )
    
    def test_create_food_truck_profile(self):
        """Test creating a food truck owner profile."""
        profile = FoodTruckOwnerProfile.objects.create(
            user=self.user,
            business_name='Best Tacos Ever',
            business_license='BL123456',
            cuisine_type='Mexican',
            operating_hours='Mon-Fri 11AM-3PM',
            is_verified=True
        )
        
        self.assertEqual(profile.business_name, 'Best Tacos Ever')
        self.assertEqual(profile.business_license, 'BL123456')
        self.assertEqual(profile.cuisine_type, 'Mexican')
        self.assertTrue(profile.is_verified)
        self.assertEqual(str(profile), 'Best Tacos Ever - truckowner')
        
        # Test the relationship
        self.assertEqual(self.user.food_truck_profile, profile)
    
    def test_profile_default_verification(self):
        """Test that profiles are not verified by default."""
        profile = FoodTruckOwnerProfile.objects.create(
            user=self.user,
            business_name='New Truck'
        )
        self.assertFalse(profile.is_verified)


class WebsiteUserProfileTest(TestCase):
    """
    Test cases for the WebsiteUserProfile model.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='webuser',
            email='user@example.com',
            password='userpass123',
            role='website_user'
        )
    
    def test_create_website_user_profile(self):
        """Test creating a website user profile."""
        profile = WebsiteUserProfile.objects.create(
            user=self.user,
            dietary_preferences='Vegetarian',
            favorite_cuisine_types='Italian, Thai, Mexican',
            notification_preferences=False
        )
        
        self.assertEqual(profile.dietary_preferences, 'Vegetarian')
        self.assertEqual(profile.favorite_cuisine_types, 'Italian, Thai, Mexican')
        self.assertFalse(profile.notification_preferences)
        self.assertEqual(str(profile), 'Profile for webuser')
        
        # Test the relationship
        self.assertEqual(self.user.website_user_profile, profile)
    
    def test_profile_default_notifications(self):
        """Test that notifications are enabled by default."""
        profile = WebsiteUserProfile.objects.create(
            user=self.user
        )
        self.assertTrue(profile.notification_preferences)


class UserModelIntegrationTest(TestCase):
    """
    Integration tests for the custom user model system.
    """
    
    def test_auth_user_model_setting(self):
        """Test that the AUTH_USER_MODEL setting is working."""
        from django.conf import settings
        self.assertEqual(settings.AUTH_USER_MODEL, 'directory.CustomUser')
    
    def test_get_user_model_returns_custom_user(self):
        """Test that get_user_model returns our CustomUser."""
        self.assertEqual(User, CustomUser)
    
    def test_user_authentication(self):
        """Test that authentication works with custom user model."""
        user = User.objects.create_user(
            username='authtest',
            email='auth@test.com',
            password='authpass123'
        )
        
        # Test authentication
        from django.contrib.auth import authenticate
        authenticated_user = authenticate(username='authtest', password='authpass123')
        self.assertEqual(authenticated_user, user)
        
        # Test wrong password
        wrong_auth = authenticate(username='authtest', password='wrongpass')
        self.assertIsNone(wrong_auth)
