from django.db import models
from django.contrib.auth.models import AbstractUser 


# extend user model with default abstract user
class User(AbstractUser):
    # all the field is not null and blank, everthing is required
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = None # required for the abstract user
    
    USERNAME_FIELD = "email" 
    # django authenticate with username and password but we will use email and password
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # how user raw object will return 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"    