from django.db import models
from django.contrib.auth.models import AbstractUser 


# extend user model with default abstract user
class User(AbstractUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    username = None # required for the abstract user
    
    USERNAME_FIELD = "email" 
    # django authenticate with username and password but we will use email and password
    REQUIRED_FIELDS = []

    # how user raw object will return 
    def __str__(self):
        return f"{self.name} {self.surname}"   