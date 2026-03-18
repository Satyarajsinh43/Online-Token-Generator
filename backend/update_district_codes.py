import os
import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')
django.setup()

from api.models import District

rto_mapping = {
    "Ahmedabad": "01",
    "Mehsana": "02",
    "Rajkot": "03",
    "Bhavnagar": "04",
    "Surat": "05",
    "Vadodara": "06",
    "Kheda": "07",
    "Banaskantha": "08",
    "Sabarkantha": "09",
    "Jamnagar": "10",
    "Junagadh": "11",
    "Kutch": "12",
    "Surendranagar": "13",
    "Amreli": "14",
    "Valsad": "15",
    "Bharuch": "16",
    "Panchmahal": "17",
    "Gandhinagar": "18",
    "Navsari": "21",
    "Narmada": "22",
    "Anand": "23",
    "Patan": "24",
    "Porbandar": "25",
    "Tapi": "26",
    "Ahmedabad East": "27",
    "Surat East": "28",
    "Vadodara Rural": "29",
    "Dang": "30",
    "Aravalli": "31",
    "Gir Somnath": "32",
    "Botad": "33",
    "Chhota Udepur": "34",
    "Mahisagar": "35",
    "Morbi": "36",
    "Devbhoomi Dwarka": "37"
}

print("Starting 2-step update for RTO Codes...")

try:
    with transaction.atomic():
        # Step 1: Prefix all codes to avoid unique constraint collisions
        print("Step 1: Temporary renaming...")
        all_districts = District.objects.all()
        for d in all_districts:
            d.code = f"TEMP_{d.id}_{d.code}" # Ensure uniqueness with ID
            d.save()
        print("All districts temporarily renamed.")

        # Step 2: Apply correct RTO codes
        print("Step 2: Applying RTO codes...")
        for name, code in rto_mapping.items():
            try:
                # Use iexact for case-insensitive matching
                dist = District.objects.get(name__iexact=name)
                dist.code = code
                dist.save()
                print(f"Updated {dist.name} -> {code}")
            except District.DoesNotExist:
                print(f"Skipped {name} (Not found in DB)")
        
        # Checking for any remaining TEMP codes (districts not in mapping)
        remaining = District.objects.filter(code__startswith="TEMP_")
        if remaining.exists():
            print(f"Warning: {remaining.count()} districts left with TEMP codes:")
            for r in remaining:
                # Fallback: Just use their ID or keep TEMP? 
                # Better to give them a unique code based on ID if they aren't in RTO list
                new_code = f"XX{r.id}"
                r.code = new_code
                r.save()
                print(f"  Fallback update for {r.name} -> {new_code}")

    print("Update Complete Successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
