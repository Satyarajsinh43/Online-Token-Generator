from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Profile, Office, Employee

class Command(BaseCommand):
    help = 'Creates test users for different roles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test users...')

        # Ensure at least one office exists
        office = Office.objects.first()
        if not office:
            self.stdout.write(self.style.WARNING('No office found! Creating a dummy office.'))
            office = Office.objects.create(
                office_name="Test Office",
                office_code="TEST-001",
                office_type='URBAN',
                address="Test Address"
            )

        users = [
            {
                'username': 'admin',
                'email': 'admin@gujarat.gov.in',
                'password': 'admin123',
                'role': 'SUPERADMIN',
                'is_staff': True,
                'is_superuser': True,
                'create_employee': False
            },
            {
                'username': 'office_admin',
                'email': 'office@gujarat.gov.in',
                'password': 'admin123', # simplified
                'role': 'OFFICEADMIN',
                'is_staff': True,
                'is_superuser': False,
                'create_employee': True,
                'designation': 'Office Manager'
            },
            {
                'username': 'staff',
                'email': 'staff@gujarat.gov.in',
                'password': 'staff123',
                'role': 'EMPLOYEE',
                'is_staff': False,
                'is_superuser': False,
                'create_employee': True,
                'designation': 'Clerk'
            }
        ]

        for u_data in users:
            user, created = User.objects.get_or_create(username=u_data['username'])
            user.email = u_data['email']
            user.set_password(u_data['password'])
            user.is_staff = u_data['is_staff']
            user.is_superuser = u_data['is_superuser']
            user.save()

            # Update Profile
            # Profile is created by signal, but we need to update it
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            
            user.profile.role = u_data['role']
            if u_data['create_employee']:
                user.profile.assigned_office = office
            user.profile.save()

            # Create/Update Employee Record
            if u_data['create_employee']:
                Employee.objects.get_or_create(
                    user=user,
                    defaults={
                        'office': office,
                        'designation': u_data['designation']
                    }
                )
                # Ensure office is correct if it already existed
                employee = user.employee_profile
                employee.office = office
                employee.save()

            action = "Created" if created else "Updated"
            self.stdout.write(f'{action} User: {u_data["username"]} | Email: {u_data["email"]} | Password: {u_data["password"]} | Role: {u_data["role"]}')

        self.stdout.write(self.style.SUCCESS('\nTest users created successfully!'))
        self.stdout.write(f'Office used: {office.office_name} ({office.office_type})')
