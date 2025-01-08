from django.db import models
from django.contrib.auth.models import AbstractUser 
from users.models import User
from django.core.validators import RegexValidator

# extend patient model with base User model
class Patient(User):
    gender_choices = {
        "w": "woman",
        "m": "man",
    }
    country_choices = {

    }
    city_choices = {

    }
    # r'^\+?1?\d{9,15}$'
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    gender = models.CharField(max_length=1, choices=gender_choices) 
    birthday = models.DateField()
    # no + and country code
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    country = models.CharField(max_length=3, choices=country_choices)
    city = models.CharField(max_length=1, choices=city_choices) 
    # (YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])
    created_at = models.DateTimeField(auto_now_add=True)