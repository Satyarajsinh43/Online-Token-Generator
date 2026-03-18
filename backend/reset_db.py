import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')
django.setup()

def reset_api_tables():
    with connection.cursor() as cursor:
        # 1. Drop tables if they exist (Reverse order of dependencies)
        tables = [
            'api_token',
            'api_office',
            'api_village',
            'api_taluka',
            'api_counter',
            'api_service',
            'api_district',
            'api_department',
            'api_profile',
            'api_employee',
        ]
        for table in tables:
            try:
                print(f"Dropping table {table}...")
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            except Exception as e:
                print(f"Error dropping {table}: {e}")

        # 2. Clear migration history for 'api'
        try:
            print("Clearing api migrations...")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'api';")
        except Exception as e:
            print(f"Error clearing migrations: {e}")
            
    print("Reset complete.")

if __name__ == '__main__':
    reset_api_tables()
