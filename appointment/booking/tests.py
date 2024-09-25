from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Import your models if needed
# from booking.models import YourModel

class TestViews(TestCase):

    def setUp(self):
        # Use the custom User model
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )

    def test_activation_code_email_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('activation_code_email'))
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 200)

    def test_book_appointment_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('book_appointment'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_view(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Assuming logout redirects

    def test_officer_panel_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('officer_panel'))
        self.assertEqual(response.status_code, 200)

    def test_payment_page_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('payment_page'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_track_application_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('track_application'))
        self.assertEqual(response.status_code, 200)

    def test_upload_document_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('upload_document'))
        self.assertEqual(response.status_code, 200)

    def test_user_panel_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_panel'))
        self.assertEqual(response.status_code, 200)

