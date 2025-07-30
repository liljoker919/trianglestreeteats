from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from directory.models import FoodTruck
from directory.forms import FoodTruckOwnerRegistrationForm

User = get_user_model()


class FoodTruckOwnerRegistrationFormTest(TestCase):
    """Test cases for the FoodTruckOwnerRegistrationForm."""
    
    def test_form_valid_with_minimal_data(self):
        """Test form validation with minimal required data."""
        form_data = {
            'username': 'truckowner',
            'email': 'owner@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_valid_with_full_data(self):
        """Test form validation with all fields populated."""
        form_data = {
            'username': 'truckowner',
            'email': 'owner@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone_number': '555-0123',
            'address': '123 Main St, Raleigh, NC',
            'truck_name': 'Taco Paradise',
            'truck_city': 'Raleigh',
            'truck_cuisine': 'Mexican',
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_mismatched_passwords(self):
        """Test form validation with mismatched passwords."""
        form_data = {
            'username': 'truckowner',
            'email': 'owner@truck.com',
            'password1': 'strongpassword123',
            'password2': 'differentpassword',
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_form_invalid_missing_email(self):
        """Test form validation without required email."""
        form_data = {
            'username': 'truckowner',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_save_creates_user_with_correct_role(self):
        """Test that form.save() creates user with food_truck_owner role."""
        form_data = {
            'username': 'truckowner',
            'email': 'owner@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone_number': '555-0123',
            'address': '123 Main St',
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'truckowner')
        self.assertEqual(user.email, 'owner@truck.com')
        self.assertEqual(user.role, 'food_truck_owner')
        self.assertEqual(user.phone_number, '555-0123')
        self.assertEqual(user.address, '123 Main St')
    
    def test_form_save_creates_food_truck_when_provided(self):
        """Test that form.save() creates FoodTruck when truck_name is provided."""
        form_data = {
            'username': 'truckowner',
            'email': 'owner@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'truck_name': 'Taco Paradise',
            'truck_city': 'Raleigh',
            'truck_cuisine': 'Mexican',
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        # Check that user was created correctly
        self.assertEqual(user.role, 'food_truck_owner')
        
        # Check that food truck was created
        food_trucks = FoodTruck.objects.filter(name='Taco Paradise')
        self.assertEqual(food_trucks.count(), 1)
        
        truck = food_trucks.first()
        self.assertEqual(truck.name, 'Taco Paradise')
        self.assertEqual(truck.city, 'Raleigh')
        self.assertEqual(truck.cuisine, 'Mexican')
    
    def test_form_save_no_food_truck_when_name_empty(self):
        """Test that no FoodTruck is created when truck_name is empty."""
        form_data = {
            'username': 'truckowner',
            'email': 'owner@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'truck_name': '',  # Empty truck name
        }
        form = FoodTruckOwnerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        # Check that user was created correctly
        self.assertEqual(user.role, 'food_truck_owner')
        
        # Check that no food truck was created
        self.assertEqual(FoodTruck.objects.count(), 0)


class FoodTruckOwnerRegistrationViewTest(TestCase):
    """Test cases for the food truck owner registration view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.registration_url = reverse('register_food_truck_owner')
    
    def test_registration_page_loads(self):
        """Test that the registration page loads successfully."""
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Food Truck Owner Registration')
        self.assertContains(response, 'Account Information')
        self.assertContains(response, 'Food Truck Information')
    
    def test_registration_page_uses_correct_template(self):
        """Test that the registration page uses the correct template."""
        response = self.client.get(self.registration_url)
        self.assertTemplateUsed(response, 'registration/register_food_truck_owner.html')
    
    def test_registration_page_extends_base_template(self):
        """Test that the registration page extends base.html."""
        response = self.client.get(self.registration_url)
        self.assertContains(response, 'TriAngleStreatsEats')  # From base template
        self.assertContains(response, 'navbar')  # From base template
    
    def test_successful_registration_with_minimal_data(self):
        """Test successful registration with minimal required data."""
        form_data = {
            'username': 'newtruckowner',
            'email': 'new@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # Should redirect to profile after successful registration
        self.assertRedirects(response, reverse('profile'))
        
        # Check that user was created
        user = User.objects.get(username='newtruckowner')
        self.assertEqual(user.email, 'new@truck.com')
        self.assertEqual(user.role, 'food_truck_owner')
        
        # Check that no food truck was created (no truck name provided)
        self.assertEqual(FoodTruck.objects.count(), 0)
    
    def test_successful_registration_with_truck_data(self):
        """Test successful registration with food truck information."""
        form_data = {
            'username': 'truckowner2',
            'email': 'owner2@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone_number': '555-0123',
            'address': '123 Main St',
            'truck_name': 'Burger Heaven',
            'truck_city': 'Durham',
            'truck_cuisine': 'American',
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # Should redirect to profile after successful registration
        self.assertRedirects(response, reverse('profile'))
        
        # Check that user was created with correct data
        user = User.objects.get(username='truckowner2')
        self.assertEqual(user.email, 'owner2@truck.com')
        self.assertEqual(user.role, 'food_truck_owner')
        self.assertEqual(user.phone_number, '555-0123')
        self.assertEqual(user.address, '123 Main St')
        
        # Check that food truck was created
        truck = FoodTruck.objects.get(name='Burger Heaven')
        self.assertEqual(truck.city, 'Durham')
        self.assertEqual(truck.cuisine, 'American')
    
    def test_registration_user_logged_in_after_success(self):
        """Test that user is automatically logged in after successful registration."""
        form_data = {
            'username': 'autouser',
            'email': 'auto@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # User should be logged in after registration
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'autouser')
    
    def test_registration_form_errors_displayed(self):
        """Test that form errors are displayed when registration fails."""
        form_data = {
            'username': 'baduser',
            'email': 'bademail',  # Invalid email
            'password1': 'pass',  # Weak password
            'password2': 'different',  # Mismatched password
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # Should stay on registration page and show errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register_food_truck_owner.html')
        self.assertContains(response, 'Enter a valid email address')
    
    def test_duplicate_username_registration_fails(self):
        """Test that registration fails with duplicate username."""
        # Create an existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )
        
        form_data = {
            'username': 'existinguser',  # Same username
            'email': 'new@truck.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        
        response = self.client.post(self.registration_url, data=form_data)
        
        # Should stay on registration page and show errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists')


class FoodTruckOwnerRegistrationURLTest(TestCase):
    """Test cases for food truck owner registration URL configuration."""
    
    def test_registration_url_resolves(self):
        """Test that the registration URL resolves correctly."""
        url = reverse('register_food_truck_owner')
        self.assertEqual(url, '/register/food-truck-owner/')
    
    def test_registration_url_name_works(self):
        """Test that the URL name can be used in templates and redirects."""
        # This test verifies that the URL name is properly configured
        response = self.client.get(reverse('register_food_truck_owner'))
        self.assertEqual(response.status_code, 200)


class NavigationIntegrationTest(TestCase):
    """Test cases for navigation integration with food truck owner registration."""
    
    def test_registration_dropdown_in_navigation(self):
        """Test that registration dropdown appears in navigation for unauthenticated users."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that dropdown toggle is present
        self.assertContains(response, 'dropdown-toggle')
        self.assertContains(response, 'Regular User')
        self.assertContains(response, 'Food Truck Owner')
        
        # Check that the links point to correct URLs
        self.assertContains(response, 'href="/register/"')
        self.assertContains(response, 'href="/register/food-truck-owner/"')
    
    def test_authenticated_user_no_registration_dropdown(self):
        """Test that authenticated users don't see registration dropdown."""
        # Create and log in a user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Should not see registration dropdown
        self.assertNotContains(response, 'Food Truck Owner')
        self.assertNotContains(response, 'href="/register/food-truck-owner/"')
        
        # Should see profile and logout links instead
        self.assertContains(response, 'href="/profile/"')
        self.assertContains(response, 'href="/logout/"')