from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Faculty
import sys

class Command(BaseCommand):
    help = 'Create test faculty account for dashboard testing'

    def handle(self, *args, **options):
        username = 'faculty1'
        email = 'faculty1@zainussunna.com'
        password = 'password123'
        faculty_name = 'Test Faculty'

        # Create User if not exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,  # Allow admin access
                is_superuser=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {username}')
            )

        # Create Faculty if not exists
        if Faculty.objects.filter(user=user).exists():
            self.stdout.write(
                self.style.WARNING('Faculty record already exists')
            )
        else:
            Faculty.objects.create(
                user=user,
                name=faculty_name,
                role='Ustadh',
                phone='+919876543210',
                specialization='All Subjects',
                status='active',
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created Faculty: {faculty_name}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Test Faculty Ready!\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Login URL: http://localhost:8000/api/core/faculty/login/\n'
                f'Dashboard: http://localhost:5173 (frontend)\n'
            )
        )
        print('💡 Pro tip: Run `python manage.py runserver` if backend not started')
