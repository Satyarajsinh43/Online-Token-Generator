import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')
django.setup()

from api.models import District, Taluka, Village

def import_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print("Reading file...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Cache existing districts and talukas to minimize DB hits
    # Structure: {district_name: {taluka_name: taluka_obj}}
    # But names might vary slightly, so we'll query or get_or_create carefully.
    # Given the data format is consistent, we can rely on string matching.
    
    # Existing Districts in DB (from seed_data.py)
    # We should trust the input file's district names or map them?
    # The input file has "Banas Kantha", "Sabarkantha" (maybe?).
    # let's just use get_or_create for everything to be safe.

    count_d = 0
    count_t = 0
    count_v = 0

    print(f"Processing {len(lines)} lines...")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("Sr NO") or line.startswith("List of Villages"):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        # Format: Index District Taluka Village
        # Index is parts[0]
        
        # Parsing Logic:
        # District can be 1 or 2 words (e.g., Banas Kantha, Kachchh)
        # Taluka can be 1 or 2 words
        # Village is the rest.
        
        # Heuristic:
        # Known multi-word districts: "Banas Kantha", "Sabar Kantha", "Panch Mahals", "Chhota Udepur", "Devbhumi Dwarka", "Gir Somnath"
        # We can try to match these.
        
        idx = parts[0]
        rest = parts[1:]
        
        district_name = ""
        taluka_name = ""
        village_name = ""
        
        # Detect District
        if rest[0] == "Banas" and rest[1] == "Kantha":
            district_name = "Banas Kantha"
            rest = rest[2:]
        elif rest[0] == "Sabar" and rest[1] == "Kantha":
            district_name = "Sabar Kantha"
            rest = rest[2:]
        elif rest[0] == "Panch" and rest[1] == "Mahals":
            district_name = "Panch Mahals" # specific check needed if it appears
            rest = rest[2:]
        elif rest[0] == "Chhota" and rest[1] == "Udepur":
             district_name = "Chhota Udepur"
             rest = rest[2:]
        # Add other two-word districts if found in the file
        else:
            district_name = rest[0]
            rest = rest[1:]

        # Detect Taluka
        # Taluka is usually the next word. But some might be two words?
        # Let's assume 1 word for now unless we see patterns.
        # In the provided snippet: "Vav", "Tharad", "Dhanera", "Dantiwada", "Amirgadh", "Danta", "Vadgam", "Palanpur", "Deesa", "Deodar", "Bhabhar", "Kankrej", "Santalpur", "Radhanpur", "Sidhpur", "Patan", "Harij", "Sami", "Chanasma", "Satlasana", "Kheralu", "Unjha", "Visnagar", "Vadnagar", "Vijapur", "Mahesana", "Becharaji", "Kadi", "Khedbrahma", "Vijaynagar", "Vadali", "Idar"
        # Most are 1 word.
        # "Ahmedabad City" is 2 words.
        
        # Let's check if the NEXT word looks like a known taluka or generic.
        # For this specific dataset, names seem to be single words mostly or hyphenated?
        # Actually "Ahmedabad City" might not be in this "List of Villages" format if it's rural only?
        # Let's assume Taluka is the NEXT token.
        
        taluka_name = rest[0]
        rest = rest[1:]
        
        # The rest is village name
        village_name = " ".join(rest)
        
        # Cleanup
        # Remove anything in parenthesis or extra chars if needed.
        
        # DB Operations
        # 1. District
        # We try to get the existing district first (from seed_data).
        # Note: seed_data used "Banaskantha" (one word)? or "Banas Kantha"?
        # Ensure we match or create.
        
        dist_obj, created_d = District.objects.get_or_create(name=district_name)
        if created_d:
             # Generate code if new
             dist_obj.code = str(District.objects.count()).zfill(2)
             dist_obj.save()
             count_d += 1

        # 2. Taluka
        tal_obj, created_t = Taluka.objects.get_or_create(name=taluka_name, district=dist_obj)
        if created_t:
            count_t += 1

        # 3. Village
        vil_obj, created_v = Village.objects.get_or_create(name=village_name, taluka=tal_obj)
        if created_v:
            count_v += 1
            
            # 4. Create default Office (Gram Panchayat)
            # Only create if it's a new village
            from api.models import Office
            Office.objects.get_or_create(
                office_name=f"Gram Panchayat {village_name}",
                office_type='RURAL',
                office_code=f"GP_VIL_{vil_obj.id}",
                district=dist_obj,
                taluka=tal_obj,
                village=vil_obj,
                defaults={"address": f"Main Chowk, {village_name}"}
            )

    print("Import Completed!")
    print(f"New Districts: {count_d}")
    print(f"New Talukas: {count_t}")
    print(f"New Villages: {count_v}")

if __name__ == "__main__":
    import_data('villages.txt')
