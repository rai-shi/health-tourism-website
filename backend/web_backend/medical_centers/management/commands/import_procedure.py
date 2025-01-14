# medical_center/management/commands/import_specialities.py

from django.core.management.base import BaseCommand
from medical_centers.models import Procedure, Speciality
import os
from django.conf import settings  
from pathlib import Path  

class Command(BaseCommand):
    help = 'Import specialities from a .txt file into the database'

    def handle(self, *args, **kwargs):
        file_path = Path(settings.BASE_DIR) / 'medical_centers' / 'management' / 'commands' / 'procedure_list.txt'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File does not exist: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                striptedLine = line.strip() 
                words = striptedLine.split(",")
                name = words[0] 
                code = words[1] 
                speciality_code = words[2] 
                # if record is not already exist
                if not Procedure.objects.filter(name=name).exists():
                    
                    # if related speciality exist
                    if Speciality.objects.filter(code=speciality_code).exists():
                        # create the procedure
                        speciality = Speciality.objects.filter(code=speciality_code).first()
                        Procedure.objects.create(name=name,
                                                code=code,
                                                speciality_code=speciality)
                        self.stdout.write(self.style.SUCCESS(f'Successfully added speciality: {name}'))
                    else:
                        self.stdout.write(self.style.NOTICE(f'There is no {speciality_code} speciality for the procedure {name}. Please record speciailty first.'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Procedure already exists: {name}'))

        self.stdout.write(self.style.SUCCESS('Import completed'))



# text = """Angiography
# Atherectomy
# Balloon valvuloplasty
# Coronary angioplasty
# Coronary artery bypass grafting (CABG)
# Coronary stenting
# Heart transplantation
# Hybrid operating room
# Pacemaker implantation
# Pediatric heart surgery
# Rotablation
# Surgical aneurysm repair
# Valve replacement"""

# result = []
# lines = text.split("\n")
# for idx, line in enumerate(lines):

#     new_line = line + ",CS-"+ str(idx+1) + ",CS"
#     result.append(new_line)
#     print(new_line)

# finish_text = "\n".join(result)

