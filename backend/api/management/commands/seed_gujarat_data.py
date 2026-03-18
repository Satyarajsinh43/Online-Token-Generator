from django.core.management.base import BaseCommand
from api.models import District, Taluka, Village, Office
import random

class Command(BaseCommand):
    help = 'Seeds Gujarat data with complete hierarchy.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Gujarat Data...')

        # Sample Data Structure: District -> [Talukas]
        # In a real scenario, this would be a full JSON of 33 districts.
        # Here we seed a representative subset for demonstration as per constraints.
        
        gujarat_data = {
            'Ahmedabad': ['Ahmedabad City', 'Daskroi', 'Sanand', 'Bavla', 'Dholka'],
            'Gandhinagar': ['Gandhinagar', 'Kalol', 'Dehgam', 'Mansa'],
            'Surat': ['Surat City', 'Choryasi', 'Olpad', 'Kamrej', 'Mangrol'],
            'Rajkot': ['Rajkot', 'Gondal', 'Jetpur', 'Dhoraji'],
            'Vadodara': ['Vadodara', 'Padra', 'Karjan', 'Dabhoi'],
            'Bhavnagar': ['Bhavnagar', 'Mahuva', 'Talaja', 'Palitana'],
            'Jamnagar': ['Jamnagar', 'Dhrol', 'Jodiya'],
            'Junagadh': ['Junagadh', 'Keshod', 'Mangrol'],
             # Add more as needed... 33 districts is a lot for a script, this proves hierarchy.
        }

        # Common Villages for Rural Offices
        villages_list = ['Rampur', 'Laxmipur', 'Sultanpur', 'Isanpur', 'Govindpur']

        for dist_name, talukas in gujarat_data.items():
            district, _ = District.objects.get_or_create(
                name=dist_name, 
                defaults={'code': f"GJ-{dist_name[:3].upper()}"}
            )
            self.stdout.write(f"Processing District: {dist_name}")

            for taluka_name in talukas:
                taluka, _ = Taluka.objects.get_or_create(name=taluka_name, district=district)

                # 1. Create Urban Office (City Civic Center) in main talukas (heuristic)
                # Usually "City" talukas or main district talukas have urban centers.
                # We will create an URBAN office in EVERY taluka for demo purposes
                Office.objects.get_or_create(
                    office_name=f"{taluka_name} Civic Center",
                    office_code=f"OFF-{taluka_name[:3].upper()}-{random_suffix()}",
                    district=district,
                    taluka=taluka,
                    office_type='URBAN',
                    defaults={'address': f"Main Bazar, {taluka_name}"}
                )

                # 2. Create Villages and Rural Offices
                for v_name in villages_list:
                    village, _ = Village.objects.get_or_create(
                        name=f"{v_name} ({taluka_name})", 
                        taluka=taluka
                    )
                    
                    # Create Rural Office - Gram Panchayat
                    Office.objects.get_or_create(
                        office_name=f"Gram Panchayat {v_name}",
                        office_code=f"GP-{v_name[:3].upper()}-{random_suffix()}",
                        district=district,
                        taluka=taluka,
                        village=village,
                        office_type='RURAL',
                        defaults={'address': f"Panchayat Bhavan, {village.name}"}
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Gujarat hierarchy.'))

def random_suffix():
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
