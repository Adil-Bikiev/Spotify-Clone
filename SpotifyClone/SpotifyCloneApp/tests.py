from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class SpotifyCloneAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.email = "test@example.com"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_signup_view_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertRedirects(response, reverse('user_in'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'wrongpassword'
        })
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('user_in'))

    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertRedirects(response, reverse('login'))

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_user_in_view_requires_login(self):
        response = self.client.get(reverse('user_in'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('user_in')}")

    def test_library_user_view_fetches_artists(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('library_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'SpotifyCloneApp/library.html')
