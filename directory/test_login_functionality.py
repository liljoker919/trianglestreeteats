from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.conf import settings

User = get_user_model()


class LoginFunctionalityTest(TestCase):
    """Test cases for login functionality implementation."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_page_renders_form(self):
        """Test that login page renders with a proper form."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        
        # Check that form elements are present
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'type="submit"')

    def test_login_page_has_required_elements(self):
        """Test that login page has all required UI elements."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        
        # Check for proper labels and structure
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Back to Home')
        self.assertContains(response, 'Register here')

    def test_successful_login_redirects_to_home(self):
        """Test that successful login redirects to LOGIN_REDIRECT_URL."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Should redirect to LOGIN_REDIRECT_URL
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_successful_login_authenticates_user(self):
        """Test that successful login actually authenticates the user."""
        # Ensure user is not authenticated initially
        response = self.client.get(self.home_url)
        self.assertContains(response, 'href="/login/"')
        
        # Login
        self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Check that user is now authenticated
        response = self.client.get(self.home_url)
        self.assertContains(response, 'href="/logout/"')
        self.assertNotContains(response, 'href="/login/"')

    def test_successful_login_shows_success_message(self):
        """Test that successful login shows a welcome message."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)
        
        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Welcome back' in str(message) for message in messages))

    def test_invalid_credentials_shows_error(self):
        """Test that invalid credentials show appropriate error."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should not redirect (stay on login page)
        self.assertEqual(response.status_code, 200)
        
        # Check for error message or form errors
        messages = list(get_messages(response.wsgi_request))
        has_message_error = any('correct the errors' in str(message) for message in messages)
        has_form_error = 'form' in response.context and response.context['form'].errors
        self.assertTrue(has_message_error or has_form_error)

    def test_nonexistent_user_shows_error(self):
        """Test that nonexistent user shows appropriate error."""
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': 'anypassword'
        })
        
        # Should not redirect (stay on login page)
        self.assertEqual(response.status_code, 200)
        
        # Check for error message in form or messages
        messages = list(get_messages(response.wsgi_request))
        has_message_error = any('correct the errors' in str(message) for message in messages)
        has_form_error = 'form' in response.context and response.context['form'].errors
        self.assertTrue(has_message_error or has_form_error)

    def test_empty_form_shows_validation_errors(self):
        """Test that empty form submission shows validation errors."""
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        
        # Should not redirect (stay on login page)
        self.assertEqual(response.status_code, 200)
        
        # Check that form has errors
        self.assertTrue(response.context['form'].errors)

    def test_missing_username_shows_validation_error(self):
        """Test that missing username shows validation error."""
        response = self.client.post(self.login_url, {
            'username': '',
            'password': 'testpass123'
        })
        
        # Should not redirect (stay on login page)
        self.assertEqual(response.status_code, 200)
        
        # Check that form has username error
        self.assertTrue('username' in response.context['form'].errors)

    def test_missing_password_shows_validation_error(self):
        """Test that missing password shows validation error."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': ''
        })
        
        # Should not redirect (stay on login page)
        self.assertEqual(response.status_code, 200)
        
        # Check that form has password error
        self.assertTrue('password' in response.context['form'].errors)

    def test_login_page_extends_base_template(self):
        """Test that login page properly extends base template."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        
        # Check for base template elements
        self.assertContains(response, 'TriAngleStreatsEats')  # navbar brand
        self.assertContains(response, 'navbar')
        
    def test_login_redirects_authenticated_user(self):
        """Test that already authenticated users can still access login page."""
        # Login the user first
        self.client.login(username='testuser', password='testpass123')
        
        # Access login page
        response = self.client.get(self.login_url)
        
        # Should still show the login page (Django's default behavior)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_form_maintains_data_on_error(self):
        """Test that form maintains username data when there's an error."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should maintain username in form
        self.assertContains(response, 'value="testuser"')