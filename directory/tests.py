from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser, FoodTruckOwnerProfile, WebsiteUserProfile, FoodTruck

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


class FoodTruckModelTest(TestCase):
    """
    Test cases for the FoodTruck model.
    """
    
    def test_create_food_truck_required_fields_only(self):
        """Test creating a food truck with only required fields."""
        truck = FoodTruck.objects.create(
            name='Taco Paradise',
            city='Raleigh',
            cuisine='Mexican'
        )
        
        self.assertEqual(truck.name, 'Taco Paradise')
        self.assertEqual(truck.city, 'Raleigh')
        self.assertEqual(truck.cuisine, 'Mexican')
        self.assertEqual(str(truck), 'Taco Paradise')
        
        # Test optional fields are None/empty
        self.assertIsNone(truck.description)
        self.assertIsNone(truck.website)
        self.assertIsNone(truck.social_links)
        self.assertFalse(truck.image)  # ImageField is falsy when empty
    
    def test_create_food_truck_all_fields(self):
        """Test creating a food truck with all fields populated."""
        social_links_data = {
            'facebook': 'https://facebook.com/tacoparadise',
            'instagram': 'https://instagram.com/tacoparadise',
            'twitter': 'https://twitter.com/tacoparadise'
        }
        
        truck = FoodTruck.objects.create(
            name='Gourmet Burgers',
            city='Durham',
            cuisine='American',
            description='The best gourmet burgers in the Triangle area',
            website='https://gourmetburgers.com',
            social_links=social_links_data
        )
        
        self.assertEqual(truck.name, 'Gourmet Burgers')
        self.assertEqual(truck.city, 'Durham')
        self.assertEqual(truck.cuisine, 'American')
        self.assertEqual(truck.description, 'The best gourmet burgers in the Triangle area')
        self.assertEqual(truck.website, 'https://gourmetburgers.com')
        self.assertEqual(truck.social_links, social_links_data)
        self.assertEqual(str(truck), 'Gourmet Burgers')
    
    def test_food_truck_name_max_length(self):
        """Test that name field respects max_length."""
        # Test name at max length (100 characters)
        long_name = 'A' * 100
        truck = FoodTruck.objects.create(
            name=long_name,
            city='Chapel Hill',
            cuisine='Italian'
        )
        self.assertEqual(truck.name, long_name)
        self.assertEqual(len(truck.name), 100)
    
    def test_food_truck_city_max_length(self):
        """Test that city field respects max_length."""
        # Test city at max length (50 characters)
        long_city = 'B' * 50
        truck = FoodTruck.objects.create(
            name='Pizza Palace',
            city=long_city,
            cuisine='Italian'
        )
        self.assertEqual(truck.city, long_city)
        self.assertEqual(len(truck.city), 50)
    
    def test_food_truck_cuisine_max_length(self):
        """Test that cuisine field respects max_length."""
        # Test cuisine at max length (50 characters)
        long_cuisine = 'C' * 50
        truck = FoodTruck.objects.create(
            name='Fusion Food',
            city='Cary',
            cuisine=long_cuisine
        )
        self.assertEqual(truck.cuisine, long_cuisine)
        self.assertEqual(len(truck.cuisine), 50)
    
    def test_food_truck_json_field_structure(self):
        """Test that social_links JSONField can store structured data."""
        social_data = {
            'facebook': 'https://facebook.com/test',
            'instagram': 'https://instagram.com/test',
            'twitter': 'https://twitter.com/test',
            'website': 'https://test.com'
        }
        
        truck = FoodTruck.objects.create(
            name='Test Truck',
            city='Test City',
            cuisine='Test Cuisine',
            social_links=social_data
        )
        
        # Retrieve from database to ensure it's properly stored/retrieved
        retrieved_truck = FoodTruck.objects.get(id=truck.id)
        self.assertEqual(retrieved_truck.social_links, social_data)
        self.assertEqual(retrieved_truck.social_links['facebook'], 'https://facebook.com/test')
    
    def test_food_truck_optional_fields_can_be_empty(self):
        """Test that optional fields can be explicitly set to empty values."""
        truck = FoodTruck.objects.create(
            name='Minimal Truck',
            city='Minimal City',
            cuisine='Minimal Cuisine',
            description='',
            website='',
            social_links={}
        )
        
        self.assertEqual(truck.description, '')
        self.assertEqual(truck.website, '')
        self.assertEqual(truck.social_links, {})
        
    def test_multiple_food_trucks(self):
        """Test creating multiple food trucks to ensure no conflicts."""
        truck1 = FoodTruck.objects.create(
            name='Truck One',
            city='City One',
            cuisine='Cuisine One'
        )
        
        truck2 = FoodTruck.objects.create(
            name='Truck Two',
            city='City Two',
            cuisine='Cuisine Two'
        )
        
        trucks = FoodTruck.objects.all()
        self.assertEqual(trucks.count(), 2)
        self.assertIn(truck1, trucks)
        self.assertIn(truck2, trucks)
