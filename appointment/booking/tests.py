from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Appointment, Notification

class UserPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.officer = User.objects.create_user(username='officer', password='password', role='officer')
        
        # Create test appointments
        self.appointment = Appointment.objects.create(user=self.user, date='2024-07-01', time='10:00')
        
        # Create test notifications
        self.notification = Notification.objects.create(appointment=self.appointment, message='Test notification')

    def test_login_required(self):
        response = self.client.get(reverse('user_information'))
        self.assertRedirects(response, '/accounts/login/?next=/user-information/')

    def test_user_information_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.get(reverse('user_information'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Information')

    def test_manage_appointments_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.get(reverse('manage_appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manage Appointments')

    def test_edit_appointment_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.get(reverse('edit_appointment', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Appointment')

    def test_delete_appointment_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.post(reverse('delete_appointment', args=[self.appointment.id]))
        self.assertRedirects(response, reverse('manage_appointments'))
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())

    def test_edit_user_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.get(reverse('edit_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit User')

    def test_delete_user_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.post(reverse('delete_user', args=[self.user.id]))
        self.assertRedirects(response, reverse('user_information'))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_notifications_view(self):
        self.client.login(username='officer', password='password')
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notifications')
        self.assertContains(response, 'Test notification')

    def test_unauthorized_access(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('manage_appointments'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('user_information'))
        self.assertEqual(response.status_code, 403)
