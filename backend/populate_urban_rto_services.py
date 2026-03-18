
import os
import django
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "token_generator.settings")
django.setup()

from api.models import District, Taluka, Office, Service

def populate_data():
    # with transaction.atomic():  <-- REMOVED to allow individual errors without rollback
    print("Starting data population...")

    # 1. Populate URBAN Offices (City Civic Centers)
    talukas = Taluka.objects.all()
    print(f"Checking {talukas.count()} Talukas for Urban offices...")
    
    urban_created = 0
    for taluka in talukas:
        office_name = f"City Civic Center {taluka.name}"
        office_code = f"CCC-{taluka.id}"
        
        try:
            Office.objects.create(
                office_name=office_name,
                office_code=office_code,
                office_type='URBAN',
                district=taluka.district,
                taluka=taluka,
                # No village for Urban
                address=f"City Civic Center, {taluka.name}, {taluka.district.name}"
            )
            urban_created += 1
        except Exception as e:
            print(f"Skipping URBAN {office_name}: {e}")
            pass
    
    print(f"Created {urban_created} new URBAN offices.")

    # 2. Populate RTO Offices
    districts = District.objects.all()
    print(f"Checking {districts.count()} Districts for RTO offices...")
    
    rto_created = 0
    for district in districts:
        office_name = f"RTO {district.name}"
        # Use district RTO code if available, else ID
        code_suffix = district.rto_code if district.rto_code else str(district.id)
        office_code = f"RTO-{code_suffix}"
        
        try:
            Office.objects.create(
                office_name=office_name,
                office_code=office_code,
                office_type='RTO',
                district=district,
                # No taluka/village for RTO usually (district level)
                address=f"RTO Office, {district.name}"
            )
            rto_created += 1
        except Exception as e:
            print(f"Skipping RTO {office_name}: {e}")
            pass
    
    print(f"Created {rto_created} RTO offices.")

    # 3. Populate Services
    services_data = [
        # RURAL
        {'name': 'Income Certificate', 'type': 'RURAL', 'time': 15},
        {'name': 'Caste Certificate', 'type': 'RURAL', 'time': 20},
        {'name': 'Non-Creamylayer Certificate', 'type': 'RURAL', 'time': 20},
        {'name': 'Domicile Certificate', 'type': 'RURAL', 'time': 15},
        {'name': 'Character Certificate', 'type': 'RURAL', 'time': 10},
        
        # URBAN
        {'name': 'Property Tax Payment', 'type': 'URBAN', 'time': 10},
        {'name': 'Professional Tax Registration', 'type': 'URBAN', 'time': 25},
        {'name': 'Shop & Establishment License', 'type': 'URBAN', 'time': 30},
        {'name': 'Birth/Death Certificate', 'type': 'URBAN', 'time': 15},
        {'name': 'Marriage Registration', 'type': 'URBAN', 'time': 45},
        
        # RTO
        {'name': 'Learner License', 'type': 'RTO', 'time': 30},
        {'name': 'Driving License Test', 'type': 'RTO', 'time': 60},
        {'name': 'Vehicle Registration', 'type': 'RTO', 'time': 45},
        {'name': 'Fitness Certificate', 'type': 'RTO', 'time': 40},
        {'name': 'Transfer of Ownership', 'type': 'RTO', 'time': 30},
    ]
    
    print(f"Checking {len(services_data)} Services...")
    srv_created = 0
    for srv in services_data:
        obj, created = Service.objects.get_or_create(
            name=srv['name'],
            office_type=srv['type'],
            defaults={'avg_time_minutes': srv['time']}
        )
        if created:
            srv_created += 1
    
    print(f"Created {srv_created} Services.")
    print("Data population complete!")

if __name__ == "__main__":
    populate_data()
