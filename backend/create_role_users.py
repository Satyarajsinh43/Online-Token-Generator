import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Profile, Office, Employee

def create_or_update_users():
    print("Beginning User Update Script...")

    office = Office.objects.first()

    users_to_setup = [
        {'email': 'admin@gujarat.gov.in', 'pass': 'admin123', 'role': 'SUPERADMIN', 'is_staff': True, 'first': 'Super', 'last': 'Admin', 'username': 'admin_gujarat'},
        {'email': 'office@gujarat.gov.in', 'pass': 'admin123', 'role': 'OFFICEADMIN', 'is_staff': True, 'first': 'Office', 'last': 'Admin', 'username': 'office_gujarat'},
        {'email': 'staff@gujarat.gov.in', 'pass': 'staff123', 'role': 'EMPLOYEE', 'is_staff': True, 'first': 'Staff', 'last': 'Member', 'username': 'staff_gujarat'}
    ]

    for data in users_to_setup:
        user = User.objects.filter(email=data['email']).first()
        if not user:
            # Fallback to check username if email missing
            user = User.objects.filter(username=data['username']).first()

        if not user:
            print(f"Creating user {data['email']}...")
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['pass'],
                first_name=data['first'],
                last_name=data['last'],
                is_staff=data['is_staff']
            )
        else:
            print(f"Updating existing user {data['email']}...")
            user.set_password(data['pass'])
            user.is_staff = data['is_staff']
            user.save()

        # Update or Create Profile
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = data['role']
        if data['role'] in ['OFFICEADMIN', 'EMPLOYEE'] and office:
            profile.assigned_office = office
        profile.save()

        # Update or Create Employee
        if data['role'] == 'EMPLOYEE' and office:
            Employee.objects.get_or_create(
                user=user,
                defaults={'office': office, 'designation': 'Staff Interface Tester'}
            )
            print(f"Bound Employee {data['email']} to {office.office_name}")
            
    print("\nAccount Roles Successfully Synchronized.")

if __name__ == '__main__':
    create_or_update_users()
