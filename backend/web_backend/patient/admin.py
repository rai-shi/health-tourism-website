from django.contrib import admin
from .models import Patient
from .models import MedicalCenterRequest, MedicalCenterRequestFile

# Register your models here.


admin.site.register(Patient)
admin.site.register(MedicalCenterRequest)
admin.site.register(MedicalCenterRequestFile)
