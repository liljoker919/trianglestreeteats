from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationNavigationTest(TestCase):
    """Test cases for authentication navigation links and flows."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_unauthenticated_user_sees_login_register_links(self):
        """Test that unauthenticated users see Login and Register links."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that login and register links are in the response
        self.assertContains(response, 'href="/login/"')
        self.assertContains(response, 'href="/register/"')
        
        # Check that profile and logout links are NOT in the response
        self.assertNotContains(response, 'href="/profile/"')
        self.assertNotContains(response, 'href="/logout/"')

    def test_authenticated_user_sees_profile_logout_links(self):
        """Test that authenticated users see Profile and Logout links."""
        # Log in the user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that profile and logout links are in the response
        self.assertContains(response, 'href="/profile/"')
        self.assertContains(response, 'href="/logout/"')
        
        # Check that login and register links are NOT in the response
        self.assertNotContains(response, 'href="/login/"')
        self.assertNotContains(response, 'href="/register/"')

    def test_login_url_resolves(self):
        """Test that login URL resolves correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a placeholder login page')

    def test_register_url_resolves(self):
        """Test that register URL resolves correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Website User Account')

    def test_profile_url_resolves(self):
        """Test that profile URL resolves correctly."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Profile')

    def test_profile_shows_user_info_when_authenticated(self):
        """Test that profile page shows user information when authenticated."""
        # Log in the user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, testuser!')
        self.assertContains(response, 'test@example.com')

    def test_logout_redirects_to_home(self):
        """Test that logout redirects to home page."""
        # Log in the user first
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        
        # Check that user is logged out by checking home page
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'href="/login/"')
        self.assertContains(response, 'href="/register/"')

    def test_url_names_work_in_templates(self):
        """Test that URL names work correctly in templates."""
        # Test that all authentication URLs can be reversed
        self.assertEqual(reverse('login'), '/login/')
        self.assertEqual(reverse('logout'), '/logout/')
        self.assertEqual(reverse('register'), '/register/')
        self.assertEqual(reverse('profile'), '/profile/')