import csv
import os
from django.core.management.base import BaseCommand
from api.models import District, Taluka, Village, Office
from django.conf import settings
from django.db import transaction

class Command(BaseCommand):
    help = 'Import Gujarat locations from CSV file (Census Format)'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'gujarat_locations.csv')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {file_path}'))
            return

        # Clean existing data to avoid conflicts
        self.stdout.write('Cleaning existing geographical data...')
        # Note: Deleting Districts will cascade delete Talukas and Villages.
        # But we need to be careful about Offices referencing them.
        # Offices have on_delete=SET_NULL or CASCADE depending on field.
        # Check models.py: 
        # District -> CASCADE for Office (wait, no)
        # Office definition:
        # district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
        # So deleting District will delete Offices linked to it! 
        # That might be undesirable if we want to keep offices but just update their links?
        # But the user asked to "Import locations". 
        # If we have dummy data, best to wipe it.
        
        # Non-interactive mode: Skip deletion and confirmation
        self.stdout.write('Starting safely import (upsert mode)...')

        with transaction.atomic():
            # REMOVED: District.objects.all().delete()
            # We will use get_or_create to preserve existing data

            self.stdout.write(f'Importing locations from {file_path}...')
            
            districts_cache = {}
            talukas_cache = {} 
            
            d_created_count = 0
            t_created_count = 0
            v_created_count = 0

            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                # Skip first 5 lines of metadata/headers
                for _ in range(5):
                    next(reader, None)

                for row in reader:
                    if not row or len(row) < 8: 
                        continue 

                    # Index 1: District Code (e.g. 438)
                    # Index 2: District Name
                    # Index 4: Sub-District Name (Taluka)
                    # Index 7: Village Name (English)
                    
                    dist_code = row[1].strip()
                    dist_name = row[2].strip()
                    taluka_name = row[4].strip()
                    village_name = row[7].strip()

                    if not dist_name or not taluka_name:
                        continue

                    # 1. District
                    if dist_name not in districts_cache:
                        # Use the CSV code or generate a safe one if missing
                        code = dist_code if dist_code else f"GJ-{dist_name[:3].upper()}"
                        
                        district, created = District.objects.get_or_create(
                            name=dist_name, 
                            defaults={'code': code} 
                        )
                        # Identify if we had a collision on name but different code? 
                        # Unlikely for District Name unique constraint.
                        
                        districts_cache[dist_name] = district
                        if created: d_created_count += 1
                    
                    district = districts_cache[dist_name]

                    # 2. Taluka
                    taluka_key = (taluka_name, district.id)
                    if taluka_key not in talukas_cache:
                        taluka, created = Taluka.objects.get_or_create(
                            name=taluka_name,
                            district=district
                        )
                        talukas_cache[taluka_key] = taluka
                        if created: t_created_count += 1
                    
                    taluka = talukas_cache[taluka_key]

                    # 3. Village
                    if village_name: 
                        village, created = Village.objects.get_or_create(
                            name=village_name,
                            taluka=taluka
                        )
                        if created: v_created_count += 1

                    if (v_created_count % 500) == 0:
                        self.stdout.write(f"Processed... {v_created_count} villages", ending='\r')

            self.stdout.write(self.style.SUCCESS(f'\nGujarat locations imported successfully'))
            self.stdout.write(f"Districts Created: {d_created_count}")
            self.stdout.write(f"Talukas Created: {t_created_count}")
            self.stdout.write(f"Villages Created: {v_created_count}")
