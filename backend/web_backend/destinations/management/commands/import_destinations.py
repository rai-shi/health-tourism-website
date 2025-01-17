# medical_center/management/commands/import_specialities.py

from django.core.management.base import BaseCommand
from destinations.models import Destination
import os
from django.conf import settings  
from pathlib import Path  

class Command(BaseCommand):
    help = 'Import specialities from a .txt file into the database'

    def handle(self, *args, **kwargs):
        file_path = Path(settings.BASE_DIR) / 'destinations' / 'management' / 'commands' / 'destinations.txt'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File does not exist: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                name = line.strip() 
                
                if not Destination.objects.filter(name=name).exists():
                    Destination.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added speciality: {name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Speciality already exists: {name}'))

        self.stdout.write(self.style.SUCCESS('Import completed'))
