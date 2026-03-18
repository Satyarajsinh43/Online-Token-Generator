from django.core.management.base import BaseCommand
from api.models import Service, Office, District

class Command(BaseCommand):
    help = 'Seed Services and RTO Offices'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Services and RTOs...')

        # 1. Seed Services
        services_data = [
            # Urban Services
            {'name': 'Income Certificate', 'office_type': 'URBAN', 'time': 15},
            {'name': 'Caste Certificate', 'office_type': 'URBAN', 'time': 20},
            {'name': 'Non-Creamy Layer Certificate', 'office_type': 'URBAN', 'time': 20},
            {'name': 'Domicile Certificate', 'office_type': 'URBAN', 'time': 15},
            {'name': 'Senior Citizen Certificate', 'office_type': 'URBAN', 'time': 10},
            {'name': 'Ration Card Service', 'office_type': 'URBAN', 'time': 30},

            # Rural Services
            {'name': 'Birth Certificate', 'office_type': 'RURAL', 'time': 15},
            {'name': 'Death Certificate', 'office_type': 'RURAL', 'time': 15},
            {'name': 'Marriage Certificate', 'office_type': 'RURAL', 'time': 25},
            {'name': 'Property Tax Assessment', 'office_type': 'RURAL', 'time': 20},
            {'name': 'BPL Certificate', 'office_type': 'RURAL', 'time': 15},
            {'name': 'Character Certificate', 'office_type': 'RURAL', 'time': 10},

            # RTO Services
            {'name': 'Learner License', 'office_type': 'RTO', 'time': 30},
            {'name': 'Permanent Driving License', 'office_type': 'RTO', 'time': 45},
            {'name': 'Vehicle Registration (RC)', 'office_type': 'RTO', 'time': 40},
            {'name': 'Vehicle Transfer', 'office_type': 'RTO', 'time': 35},
            {'name': 'Fitness Certificate', 'office_type': 'RTO', 'time': 30},
            {'name': 'Permit Application', 'office_type': 'RTO', 'time': 25},
        ]

        for svc in services_data:
            Service.objects.get_or_create(
                name=svc['name'],
                office_type=svc['office_type'],
                defaults={'avg_time_minutes': svc['time']}
            )
        self.stdout.write(self.style.SUCCESS('Services seeded.'))

        # 2. Seed RTO Offices (One per District)
        districts = District.objects.all()
        rto_count = 0
        for dist in districts:
            code = f"{dist.code}-RTO"
            rto, created = Office.objects.get_or_create(
                office_code=code,
                defaults={
                    'office_name': f"RTO Office, {dist.name}",
                    'office_type': 'RTO',
                    'district': dist,
                    'address': f"RTO Office, Near Highway, {dist.name}"
                }
            )
            if created: rto_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Seeded {rto_count} RTO Offices.'))
