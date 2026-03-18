import random
from django.core.management.base import BaseCommand
from api.models import District, Taluka, Village, Office
from django.db import transaction

class Command(BaseCommand):
    help = 'Seed Urban and Rural Offices for Gujarat (All Villages)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Offices for ALL villages...')
        
        total_created = 0
        
        # 1. District Level Offices (Urban)
        # (Keeping existing logic for Urban as it's small scale and idempotent via get_or_create)
        districts = District.objects.all()
        self.stdout.write(f"Processing Urban Offices for {districts.count()} Districts...")
        
        for dist in districts:
            # Collector Office
            code = f"{dist.code}-COL"
            Office.objects.get_or_create(
                office_code=code,
                defaults={
                    'office_name': f"Collector Office, {dist.name}",
                    'office_type': 'URBAN',
                    'district': dist,
                    'address': f"District Seva Sadan, {dist.name}"
                }
            )
            
            # DDO Office
            code_ddo = f"{dist.code}-DDO"
            Office.objects.get_or_create(
                office_code=code_ddo,
                defaults={
                    'office_name': f"District Panchayat (DDO), {dist.name}",
                    'office_type': 'URBAN',
                    'district': dist,
                    'address': f"Jilla Panchayat Bhavan, {dist.name}"
                }
            )

        # 2. Taluka Level (Urban) & Village Level (Rural)
        talukas = Taluka.objects.select_related('district').all()
        self.stdout.write(f"Processing {talukas.count()} Talukas (This may take a moment)...")

        batch_size = 1000
        offices_to_create = []

        for taluka in talukas:
            dist_short = taluka.district.code
            taluka_unique = f"TAL{taluka.id}"

            # --- Urban Taluka Offices ---
            # Mamlatdar
            code_mam = f"{dist_short}-{taluka_unique}-MAM"
            if not Office.objects.filter(office_code=code_mam).exists():
                 offices_to_create.append(Office(
                    office_name=f"Mamlatdar Office, {taluka.name}",
                    office_code=code_mam,
                    office_type='URBAN',
                    district=taluka.district,
                    taluka=taluka,
                    address=f"Taluka Seva Sadan, {taluka.name}"
                ))

            # TDO
            code_tdo = f"{dist_short}-{taluka_unique}-TDO"
            if not Office.objects.filter(office_code=code_tdo).exists():
                 offices_to_create.append(Office(
                    office_name=f"Taluka Panchayat (TDO), {taluka.name}",
                    office_code=code_tdo,
                    office_type='URBAN',
                    district=taluka.district,
                    taluka=taluka,
                    address=f"Taluka Panchayat, {taluka.name}"
                ))

            # --- Rural Village Offices (ALL VILLAGES) ---
            # Fetch all villages for this taluka
            villages = Village.objects.filter(taluka=taluka)
            
            # Optimization: check existing codes in memory to avoid N+1 DB hits
            # Construct expected codes to check existence? 
            # Or just filter existing offices for this taluka
            existing_codes = set(Office.objects.filter(taluka=taluka).values_list('office_code', flat=True))

            for village in villages:
                vil_unique = f"VIL{village.id}"
                
                # Gram Panchayat
                code_gp = f"{dist_short}-{taluka_unique}-{vil_unique}-GP"
                if code_gp not in existing_codes:
                    offices_to_create.append(Office(
                        office_name=f"Gram Panchayat, {village.name}",
                        office_code=code_gp,
                        office_type='RURAL',
                        district=taluka.district,
                        taluka=taluka,
                        village=village,
                        address=f"Gram Panchayat Bhavan, {village.name}"
                    ))
                    existing_codes.add(code_gp) # Prevent dups in same run

                # Also add e-Gram? user said "add office", let's just add GP for now to be safe/fast,
                # actually e-Gram is standard. Let's add it.
                code_vce = f"{dist_short}-{taluka_unique}-{vil_unique}-VCE"
                if code_vce not in existing_codes:
                    offices_to_create.append(Office(
                        office_name=f"e-Gram Center, {village.name}",
                        office_code=code_vce,
                        office_type='RURAL',
                        district=taluka.district,
                        taluka=taluka,
                        village=village,
                        address=f"e-Gram Vishwagram Society, {village.name}"
                    ))
                    existing_codes.add(code_vce)

            # Flush batch
            if len(offices_to_create) > batch_size:
                Office.objects.bulk_create(offices_to_create)
                total_created += len(offices_to_create)
                self.stdout.write(f"  ...created batch of {len(offices_to_create)} offices")
                offices_to_create = []

        # Final flush
        if offices_to_create:
            Office.objects.bulk_create(offices_to_create)
            total_created += len(offices_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_created} new offices for ALL villages!'))
