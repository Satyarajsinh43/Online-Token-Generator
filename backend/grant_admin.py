import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Profile, Office, Employee

def grant_roles():
    emails_to_roles = {
        'srathod363143@gmail.com': 'SUPERADMIN',
        'srathod314331@gmail.com': 'EMPLOYEE' # Making this an employee so you can test the Staff Dashboard
    }
    
    office = Office.objects.first()

    for email, role in emails_to_roles.items():
        # Get or create the user
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})
        
        user.is_staff = True if role in ['SUPERADMIN', 'OFFICEADMIN', 'EMPLOYEE'] else False
        user.save()
        
        # Get or create the Profile
        profile, p_created = Profile.objects.get_or_create(user=user)
        
        # Assign role
        profile.role = role
        if role in ['OFFICEADMIN', 'EMPLOYEE'] and office:
            profile.assigned_office = office
        profile.save()
        
        # If Employee, link office record
        if role == 'EMPLOYEE' and office:
            Employee.objects.get_or_create(
                user=user,
                defaults={'office': office, 'designation': 'Staff'}
            )
            
        print(f"Successfully assigned {role} role to {email}")

if __name__ == '__main__':
    grant_roles()
