# medical_center/management/commands/import_specialities.py

from django.core.management.base import BaseCommand
from medical_centers.models import Speciality
import os
from django.conf import settings  
from pathlib import Path  

class Command(BaseCommand):
    help = 'Import specialities from a .txt file into the database'

    def handle(self, *args, **kwargs):
        # .txt dosyasının yolunu buraya yaz
        # file_path = '/speciality_list.txt'
        file_path = Path(settings.BASE_DIR) / 'medical_centers' / 'management' / 'commands' / 'speciality_list.txt'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File does not exist: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                speciality_line = line.strip() 
                speciality_line = speciality_line.split(",")
                name = speciality_line[0] 
                code = speciality_line[1]
                # print(name, code) 
                
                if not Speciality.objects.filter(name=name).exists():
                    Speciality.objects.create(name=name, code=code)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added speciality: {name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Speciality already exists: {name}'))

        self.stdout.write(self.style.SUCCESS('Import completed'))
