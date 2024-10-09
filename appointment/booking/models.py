from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('officer', 'Police Officer'),
        ('admin', 'Super Admin'),
    ]
    email = models.CharField(max_length=100, default='user@gmail.com')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    name = models.CharField(max_length=100, default='user')  # Provide a default value
    phone = models.CharField(max_length=15, default='0000000000')  # Provide a default value
    address = models.TextField(null=True, blank=True)  # Temporarily allow null
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True) 



class Office(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_certificate = models.FileField(upload_to='static/documents/')
    proof_of_nationality = models.FileField(upload_to='static/documents/')
    passport_photos = models.FileField(upload_to='static/documents/')
    residence_permit = models.FileField(upload_to='static/documents/', blank=True, null=True)
    marriage_certificate = models.FileField(upload_to='static/documents/', blank=True, null=True)
    death_certificate = models.FileField(upload_to='static/documents/', blank=True, null=True)
    sworn_statement = models.FileField(upload_to='static/documents/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    CARD_CHOICES = (
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    officer = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Created')
    card_status = models.CharField(max_length=20, choices=CARD_CHOICES, default="pending")
    receipt_reference = models.CharField(max_length=100, null=True, blank=True)  # Add this field to store receipt reference



class MissingIDCard(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_found = models.DateField(null=True, blank=True)  # Allows any date, including no date
    id_card_image = models.ImageField(upload_to='missing_id_cards/')

    def __str__(self):
        return self.name 
@classmethod
def get_all_missing_cards(cls):
        return cls.objects.all()

def __str__(self):
        return self.name


class Notification(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.appointment}"

from django.utils import timezone

class Communication(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='communications/', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='welcome')
    location = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.title



class ContactUs(models.Model):
     message = models.CharField(max_length=255)
     email = models.EmailField(max_length=50)
     name = models.CharField(max_length=255)

class PasswordReset(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     code = models.CharField(max_length=25)