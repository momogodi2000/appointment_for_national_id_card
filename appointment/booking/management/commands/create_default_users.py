from django.core.management.base import BaseCommand
from booking.models import User

class Command(BaseCommand):
    help = 'Create default super admin and police officer'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='momo').exists():
            User.objects.create_superuser(username='momoyvan', password='momo1234', role='admin')
            self.stdout.write(self.style.SUCCESS('Successfully created super admin'))
        
        if not User.objects.filter(username='police').exists():
            User.objects.create_user(username='police', password='police1234', role='officer')
            self.stdout.write(self.style.SUCCESS('Successfully created police officer'))
