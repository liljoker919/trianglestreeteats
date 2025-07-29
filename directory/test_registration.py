from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import WebsiteUserCreationForm

User = get_user_model()


class WebsiteUserRegistrationTests(TestCase):
    """Test cases for website user registration functionality."""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_registration_form_valid_data(self):
        """Test registration form with valid data."""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = WebsiteUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_duplicate_email(self):
        """Test registration form with duplicate email."""
        # Create a user first
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='password123'
        )
        
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'test@example.com',  # Duplicate email
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = WebsiteUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('A user with this email address already exists.', form.errors['email'])

    def test_registration_form_password_mismatch(self):
        """Test registration form with password mismatch."""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword',
        }
        form = WebsiteUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_view_get(self):
        """Test GET request to registration view."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Website User Account')
        self.assertIsInstance(response.context['form'], WebsiteUserCreationForm)

    def test_registration_view_post_valid(self):
        """Test POST request to registration view with valid data."""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        response = self.client.post(self.register_url, data=form_data)
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Check that user was created
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.role, 'website_user')

    def test_registration_view_post_invalid(self):
        """Test POST request to registration view with invalid data."""
        form_data = {
            'username': '',  # Invalid: empty username
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',  # Invalid email format
            'password1': '123',  # Invalid: too short password
            'password2': '456',  # Password mismatch
        }
        response = self.client.post(self.register_url, data=form_data)
        
        # Should stay on the same page with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Website User Account')
        
        # Check that no user was created
        self.assertEqual(User.objects.count(), 0)

    def test_user_role_assignment(self):
        """Test that users are assigned the correct role upon registration."""
        form_data = {
            'username': 'websiteuser',
            'first_name': 'Website',
            'last_name': 'User',
            'email': 'website@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        
        response = self.client.post(self.register_url, data=form_data)
        user = User.objects.get(username='websiteuser')
        
        self.assertEqual(user.role, 'website_user')
        self.assertEqual(user.get_role_display(), 'Website User')

    def test_user_automatically_logged_in_after_registration(self):
        """Test that user is automatically logged in after successful registration."""
        form_data = {
            'username': 'autouser',
            'first_name': 'Auto',
            'last_name': 'User',
            'email': 'auto@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        
        response = self.client.post(self.register_url, data=form_data)
        
        # Follow the redirect
        response = self.client.get(response.url)
        
        # Check that user is logged in by checking the response context
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'autouser')