"""
WSGI config for token_generator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')

# Add backend directory to sys.path to safely import seed_data
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Automatically run migrations and seed data on startup
try:
    import django
    django.setup()
    from django.core.management import call_command
    print("Auto-startup: Running migrations...")
    call_command('migrate', interactive=False)
    print("Auto-startup: Migrations completed.")
    
    # Check if database has all offices seeded
    from api.models import Office
    if Office.objects.count() < 1200:
        print("Auto-startup: Underpopulated database detected (< 1200 offices). Seeding full data...")
        call_command('seed_data', interactive=False)
        print("Auto-startup: Database seeded successfully.")
    else:
        print("Auto-startup: Database already fully seeded. Skipping seed.")
except Exception as e:
    print(f"Auto-startup error: {e}")

application = get_wsgi_application()
