from django.db import models

from users.models import User
from destinations.models import Destination

from phonenumber_field.modelfields import PhoneNumberField
from markdownx.models import MarkdownxField

import os
from uuid import uuid4


class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name
    
class Procedure(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=15, unique=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE )

    def __str__(self):
        return self.name
    
class HealthInstitutions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class MedicalCenter(models.Model):
    CENTER_CHOICES = [
    ("Hosp", "Hospital"),
    ("Clin", "Clinic"),
    ("MedCent", "Medical Center"),
    ("UniHosp", "University Hospital"),
    ("DentClin", "Dental Clinic"),
    ("UniMedCent", "University Medical Center"),
    ("Cent", "Center"),
    ("HospGrp", "Hospital Groups"),
    ("RehabCent", "Rehabilitation Center"),
    ("ChildCent", "Children's Hospital"),
    ]

    # CITY_CHOICES = [
    #     ("IST", "İSTANBUL"),
    #     ("ANK", "ANKARA"),
    #     ("IZ", "İZMİR"),
    #     ("SM", "SAMSUN"),
    #     ("BRS", "BURSA"),
    #     ("TRZ", "TRABZON"),
    #     ("MER", "MERSİN"),
    #     ("ADA", "ADANA"),
    #     ("HAT", "HATAY"),
    #     ("KON", "KONYA"),
    #     ("KRM", "KARAMAN"),
    #     ("GAZ", "GAZİANTEP"),
    #     ("KCE", "KOCAELİ"),
    #     ("AYD", "AYDIN"),
    #     ("ERZ", "ERZURUM"),
    # ]
    # one to one relation with base User model
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name="medical_center")
    center_name     = models.CharField( max_length=200, null=True )
    center_type     = models.CharField(max_length=15, choices=CENTER_CHOICES, default="Hosp", null=True )
    # city            = models.CharField(max_length=3, choices=CITY_CHOICES, default="IST", null=True  )
    contact_number  = PhoneNumberField( null=True )
    mail_address    = models.EmailField( max_length=100, null=True )
    web_site        = models.URLField( null=True )
    # markdown
    preview_text    = MarkdownxField( null=True )
    # markdown
    # bu metin içinde kullanılan teknolojiler, akreditasyon belgeleri, sağlık turizmi belgeleri tanımlanması sağlansın
    overview_text   = MarkdownxField( null=True )

    city                            = models.ForeignKey(Destination, default=1, on_delete=models.CASCADE, related_name='medical_centers_city')
    specialities                    = models.ManyToManyField(Speciality, related_name="medical_centers_specialities" )
    procedures                      = models.ManyToManyField(Procedure, related_name="medical_centers_procedure" )
    contracted_health_institutions  = models.ManyToManyField(HealthInstitutions, related_name="medical_centers_health_inst" )

    # available_features 
    # kullanılan teknolojiler, 
    # akreditasyon belgeleri, 
    # sağlık turizmi belgeleri

    def __str__(self):
        return self.center_name

class Doctor(models.Model):
    TITLE_CHOICES = [
        ("Dr." , "Doctor"),
        ("Prof. Dr." , "Professor Doctor"),
        ("Assoc. Dr." , "Associated Doctor"),
        ("Asst. Dr." , "Assistant Professor"),
    ]
    name            = models.CharField(max_length=50)
    surname         = models.CharField(max_length=50)
    title           = models.CharField(max_length=100, choices=TITLE_CHOICES, default="Dr.", null=True )
    major           = models.CharField(max_length=100)
    minor           = models.CharField(max_length=100, null=True)
    related_center  = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f"{self.title} {self.name} {self.surname}"

class MedicalCenterVideos(models.Model):
    medical_center  = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name='medical_center_videos')
    video_name      = models.CharField( max_length=100, unique=True )
    video_link      = models.URLField(max_length=500)
    uploaded_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_name
    

def medical_center_photo_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    new_filename = f"{uuid4()}{extension}"
    return f"medical_center/{instance.medical_center.id}/photos/{new_filename}"


class MedicalCenterPhotos(models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.CASCADE, related_name='medical_center_photos'
    )
    image_name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=medical_center_photo_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name