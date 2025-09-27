from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Run migrations and collect static files for Railway deployment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Railway deployment tasks...'))
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('Database connection: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed: {e}'))
            return

        # Run migrations
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {e}'))

        # Collect static files
        try:
            self.stdout.write('Collecting static files...')
            call_command('collectstatic', '--noinput', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Static files collected'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Static files collection failed: {e}'))

        self.stdout.write(self.style.SUCCESS('Railway deployment tasks completed!'))