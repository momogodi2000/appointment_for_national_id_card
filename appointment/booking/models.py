from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('officer', 'Police Officer'),
        ('admin', 'Super Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

class Office(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    officer = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class Document(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
