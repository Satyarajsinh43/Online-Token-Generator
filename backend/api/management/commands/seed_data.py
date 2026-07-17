from django.core.management.base import BaseCommand
from api.models import District, Taluka, Village, Office

class Command(BaseCommand):
    help = 'Seeds the database with initial data for Gujarat districts, talukas, and villages.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Districts of Gujarat (Sample)
        districts_data = {
            'Ahmedabad': {'code': 'GJ01', 'cities': ['Ahmedabad City'], 'talukas': ['Daskroi', 'Sanand']},
            'Gandhinagar': {'code': 'GJ18', 'cities': ['Gandhinagar City'], 'talukas': ['Gandhinagar', 'Kalol']},
            'Surat': {'code': 'GJ05', 'cities': ['Surat City'], 'talukas': ['Choryasi', 'Olpad']},
            'Rajkot': {'code': 'GJ03', 'cities': ['Rajkot City'], 'talukas': ['Rajkot', 'Gondal']},
        }

        # Villages sample per Taluka
        villages_sample = ['Rampur', 'Laxmipur', 'Sultanpur', 'Dholka']

        for dist_name, data in districts_data.items():
            district, created = District.objects.get_or_create(name=dist_name, defaults={'code': data['code']})
            if created:
                self.stdout.write(f'Created District: {dist_name}')
            
            # Create Cities (Urban)
            for city_name in data['cities']:
                # Treat urban city center as a Taluka in our schema
                city_taluka, c_created = Taluka.objects.get_or_create(name=city_name, district=district)
                if c_created:
                    self.stdout.write(f'Created City Taluka: {city_name}')
                
                # Create Urban Office
                Office.objects.get_or_create(
                    office_name=f"{city_name} Civic Center",
                    office_code=f"OFF-{city_name[:3].upper()}-{random_code()}",
                    district=district,
                    taluka=city_taluka,
                    office_type='URBAN',
                    defaults={'address': f"Main Road, {city_name}"}
                )

            # Create Talukas (Rural)
            for taluka_name in data['talukas']:
                taluka, t_created = Taluka.objects.get_or_create(name=taluka_name, district=district)
                
                # Create Villages linked to Taluka
                for v_name in villages_sample:
                    village, v_created = Village.objects.get_or_create(name=f"{v_name} ({taluka_name})", taluka=taluka)
                    
                    if v_created:
                         # Create Rural Office
                        Office.objects.get_or_create(
                            office_name=f"Gram Panchayat {village.name}",
                            office_code=f"GP-{village.name[:3].upper()}-{random_code()}",
                            district=district,
                            taluka=taluka,
                            village=village,
                            office_type='RURAL',
                            defaults={'address': f"Village Square, {village.name}"}
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded data.'))

def random_code():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
