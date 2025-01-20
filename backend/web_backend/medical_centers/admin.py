from django.contrib import admin
from .models import Speciality, Procedure, HealthInstitutions
from .models import MedicalCenter
from .models import Doctor, MedicalCenterPhotos, MedicalCenterVideos

# Register your models here.

admin.site.register(Speciality)
admin.site.register(Procedure)
admin.site.register(HealthInstitutions)
admin.site.register(MedicalCenter)
admin.site.register(Doctor)
admin.site.register(MedicalCenterPhotos)
admin.site.register(MedicalCenterVideos)