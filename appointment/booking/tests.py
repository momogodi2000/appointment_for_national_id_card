from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Appointment, Document, MissingIDCard, Office
from .forms import CustomUserCreationForm, AuthenticationForm, ForgotPasswordForm, AppointmentForm, DocumentUploadForm, ContactUsForm

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_user_registration(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('user_panel'))

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

class AppointmentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.office = Office.objects.create(name='Main Office', address='123 Main St')
        self.appointment = Appointment.objects.create(user=self.user, office=self.office, date='2024-07-01', time='10:00:00')

    def test_create_appointment(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'user': self.user.id,
            'office': self.office.id,
            'date': '2024-07-02',
            'time': '11:00:00',
            'status': 'pending',
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('book_appointment'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creating appointment
        self.assertTrue(Appointment.objects.filter(date='2024-07-02').exists())

    def test_view_appointments(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-07-01')

class DocumentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_upload_document(self):
        self.client.login(username='testuser', password='testpass')
        with open('testfile.pdf', 'rb') as doc:
            form_data = {
                'birth_certificate': doc,
                'proof_of_nationality': doc,
                'passport_photos': doc,
            }
            form = DocumentUploadForm(data=form_data, files=form_data)
            self.assertTrue(form.is_valid())
            response = self.client.post(reverse('upload_document'), form_data)
            self.assertEqual(response.status_code, 302)  # Redirect after uploading document
            self.assertTrue(Document.objects.filter(user=self.user).exists())

    def test_view_documents(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_panel'))
        self.assertEqual(response.status_code, 200)

class ContactUsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_us_form(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'This is a test message.',
        }
        form = ContactUsForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('contact_us'), form_data)
        self.assertEqual(response.status_code, 200)

class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')

    def test_admin_login(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'adminpass'})
        self.assertEqual(response.status_code, 302)  # Redirect to admin panel
        self.assertRedirects(response, reverse('admin_panel'))

    def test_manage_users(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)

    def test_manage_appointments(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('manage_appointments'))
        self.assertEqual(response.status_code, 200)

    def test_manage_documents(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('manage_documents'))
        self.assertEqual(response.status_code, 200)

class MissingIDCardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_insert_missing_id_card(self):
        self.client.login(username='testuser', password='testpass')
        with open('testfile.jpg', 'rb') as img:
            form_data = {
                'name': 'John Doe',
                'email': 'johndoe@example.com',
                'phone': '1234567890',
                'id_card_image': img,
            }
            form = MissingIDCardForm(data=form_data, files=form_data)
            self.assertTrue(form.is_valid())
            response = self.client.post(reverse('insert_missing_id_card'), form_data)
            self.assertEqual(response.status_code, 302)  # Redirect after inserting missing ID card
            self.assertTrue(MissingIDCard.objects.filter(name='John Doe').exists())
