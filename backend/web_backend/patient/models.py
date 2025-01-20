from django.db import models
from users.models import User
from django.core.validators import RegexValidator
from cities_light.models import Country, City
from phonenumber_field.modelfields import PhoneNumberField

from medical_centers.models import MedicalCenter, Speciality, Procedure

# extend patient model with base User model
class Patient(models.Model):
    gender_choices = {
        "w": "woman",
        "m": "man",
    }
    # FIELDS
    gender          =   models.CharField(max_length=1, choices=gender_choices, default="w") 
    birthday        =   models.DateField(null=True, blank=True)
    phone_number    =   PhoneNumberField(blank=True)
    country         =   models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city            =   models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    created_at      =   models.DateTimeField(auto_now_add=True)    # (YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])
    # one to one relation with base User model
    user            =   models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# r'^\+?1?\d{9,15}$'
# phone_regex = RegexValidator(regex=r'^\d{10}$')
# message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
# ! it's not +,countrycode,number now, maybe we can add country code as seperate field 
# models.CharField(validators=[phone_regex], max_length=10, default="0000000000")  
    


class MedicalCenterRequest(models.Model):
    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="requests")
    medical_center  = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="requests")
    speciality      = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name="requests")
    procedure       = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="requests")
    
    gender_choices = {
        "w": "woman",
        "m": "man",
    }

    # PATIENT DISEASE INFORMATION
    name        = models.CharField(max_length=50)
    surname     = models.CharField(max_length=50)
    gender      = models.CharField(max_length=1, choices=gender_choices, default="w") 
    birthday    = models.DateField(null=True, blank=True)
    phone       = PhoneNumberField()
    email       = models.EmailField(max_length=100) 
    country     = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city        = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    disease_history     = models.TextField(null=True, blank=True)
    previous_disease    = models.TextField(null=True, blank=True)
    previous_surgery    = models.TextField(null=True, blank=True)
    previous_treatment  = models.TextField(null=True, blank=True)
    other_comments      = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.first_name} {self.patient.user.last_name} to {self.medical_center} for {self.speciality}-{self.procedure}"
    

class MedicalCenterRequestFile(models.Model):
    request = models.ForeignKey(MedicalCenterRequest, on_delete=models.CASCADE, related_name="files")
    file    = models.FileField(upload_to="medical_center_requests/files/")
    
    def __str__(self):
        return f"{self.request.id}-{self.id}"
    