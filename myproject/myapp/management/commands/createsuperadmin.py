from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser with user_type set to admin'

    def handle(self, *args, **options):
        User = get_user_model()
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')

        try:
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.user_type = 'admin'  # Set user_type to 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))
