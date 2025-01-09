from django.db import models
from users.models import User
from django.core.validators import RegexValidator
from cities_light.models import Country, City

# extend patient model with base User model
class Patient(models.Model):
    gender_choices = {
        "w": "woman",
        "m": "man",
    }
    # city_choices = {}

    # r'^\+?1?\d{9,15}$'
    phone_regex = RegexValidator(regex=r'^\d{10}$')
    # message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    # ! it's not +,countrycode,number now, maybe we can add country code as seperate field 
    
    # FIELDS
    gender          =   models.CharField(max_length=1, choices=gender_choices, default="w") 
    birthday        =   models.DateField(null=True, blank=True)
    phone_number    =   models.CharField(validators=[phone_regex], max_length=10, default="0000000000")  
    country         =   models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city            =   models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    created_at      =   models.DateTimeField(auto_now_add=True)    # (YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])
    # one to one relation with base User model
    user            =   models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")