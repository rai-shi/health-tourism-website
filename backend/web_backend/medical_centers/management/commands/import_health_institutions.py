# medical_center/management/commands/import_specialities.py

from django.core.management.base import BaseCommand
from medical_centers.models import HealthInstitutions
import os
from django.conf import settings  
from pathlib import Path  

class Command(BaseCommand):
    help = 'Import specialities from a .txt file into the database'

    def handle(self, *args, **kwargs):
        file_path = Path(settings.BASE_DIR) / 'medical_centers' / 'management' / 'commands' / 'health_institutions_list.txt'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File does not exist: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                stripted_line = line.strip() 
                nameandcode = stripted_line.split(",")
                name = nameandcode[0] 
                code = nameandcode[1]  
                
                if not HealthInstitutions.objects.filter(name=name, code=code).exists():
                    HealthInstitutions.objects.create(name=name, code=code)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added speciality: {name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Speciality already exists: {name}'))

        self.stdout.write(self.style.SUCCESS('Import completed'))
