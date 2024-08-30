from django.core.management.base import BaseCommand
from booking.models import User

class Command(BaseCommand):
    help = 'Create default super admin and police officer'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin1234',
                email='admin@gmail.com',  # Added email
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created super admin'))

        if not User.objects.filter(username='police').exists():
            User.objects.create_user(
                username='police',
                password='police1234',
                email='police@gmail.com',  # Added email
                role='officer'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created police officer'))