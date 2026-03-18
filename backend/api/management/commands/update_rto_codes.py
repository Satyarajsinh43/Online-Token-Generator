from django.core.management.base import BaseCommand
from api.models import District

class Command(BaseCommand):
    help = 'Updates RTO codes for districts based on standard GJ list'

    def handle(self, *args, **kwargs):
        # Map: District Name (or key part) -> RTO Code suffix
        # User provided: GJ-01 Ahmedabad, etc.
        # We store just the number string: "01", "02", etc.
        
        rto_data = [
            ("01", ["Ahmedabad"]),
            ("02", ["Mehsana"]),
            ("03", ["Rajkot"]),
            ("04", ["Bhavnagar"]),
            ("05", ["Surat"]),
            ("06", ["Vadodara"]),
            ("07", ["Kheda", "Nadiad"]),
            ("08", ["Banaskantha", "Palanpur"]),
            ("09", ["Sabarkantha", "Himmatnagar"]),
            ("10", ["Jamnagar"]),
            ("11", ["Junagadh"]),
            ("12", ["Kutch", "Bhuj"]),
            ("13", ["Surendranagar"]),
            ("14", ["Amreli"]),
            ("15", ["Valsad"]),
            ("16", ["Bharuch"]),
            ("17", ["Panchmahal", "Godhra"]),
            ("18", ["Gandhinagar"]),
            ("19", ["Bardoli", "Surat Rural"]), # Might not match if District is just Surat
            ("20", ["Dahod"]),
            ("21", ["Navsari"]),
            ("22", ["Narmada", "Rajpipla"]),
            ("23", ["Anand"]),
            ("24", ["Patan"]),
            ("25", ["Porbandar"]),
            ("26", ["Tapi", "Vyara"]),
            ("27", ["Ahmedabad East"]),
            ("28", ["Vapi"]), # Vapi is in Valsad usually, unless separate district
            ("29", ["Vadodara Rural"]),
            ("30", ["Dang", "Ahwa"]),
            ("31", ["Aravalli", "Modasa"]),
            ("32", ["Gir Somnath", "Veraval"]),
            ("33", ["Botad"]),
            ("34", ["Chhota Udaipur"]),
            ("35", ["Morbi"]),
            ("36", ["Devbhoomi Dwarka"]),
            ("37", ["Mahisagar", "Lunawada"]),
        ]

        count = 0
        for code, names in rto_data:
            # Try to find a district matching one of the names
            # We search for checking if District.name contains the keyword (case insensitive)
            
            district = None
            for name in names:
                # Exact match first
                qs = District.objects.filter(name__iexact=name)
                if qs.exists():
                    district = qs.first()
                    break
                
                # Contains match
                qs = District.objects.filter(name__icontains=name)
                if qs.exists():
                    district = qs.first()
                    break
            
            if district:
                if not district.rto_code: # Only update if empty or overwrite? User asked to set them. Let's overwrite.
                    district.rto_code = code
                    district.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated {district.name} to RTO Code {code}"))
                    count += 1
                else:
                    # Update anyway to be sure
                    district.rto_code = code
                    district.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated {district.name} to RTO Code {code}"))
                    count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Could not find District for code {code} (Checked: {names})"))

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully updated {count} districts."))
