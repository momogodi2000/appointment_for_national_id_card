from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('officer', 'Police Officer'),
        ('admin', 'Super Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    name = models.CharField(max_length=100, default='user')  # Provide a default value
    phone = models.CharField(max_length=15, default='0000000000')  # Provide a default value
    address = models.TextField(null=True, blank=True)  # Temporarily allow null

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_certificate = models.FileField(upload_to='documents/', blank=True, null=True)
    proof_of_nationality = models.FileField(upload_to='documents/', blank=True, null=True)
    passport_photos = models.FileField(upload_to='documents/', blank=True, null=True)
    residence_permit = models.FileField(upload_to='documents/', blank=True, null=True)
    marriage_certificate = models.FileField(upload_to='documents/', blank=True, null=True)
    death_certificate = models.FileField(upload_to='documents/', blank=True, null=True)
    sworn_statement = models.FileField(upload_to='documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class MissingIDCard(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    id_card_image = models.ImageField(upload_to='missing_id_cards/')
    
@classmethod
def get_all_missing_cards(cls):
        return cls.objects.all()

def __str__(self):
        return self.name

class Notification(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.appointment}"
