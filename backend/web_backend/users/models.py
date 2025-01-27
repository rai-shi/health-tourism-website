from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# since we create new User Model extended with AbstractUser, we need to override the createsuperuser command
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# extend user model with default abstract user
class User(AbstractUser):
    # all the field is not null and blank, everthing is required
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    email       = models.EmailField(max_length=100, unique=True)
    password    = models.CharField(max_length=100)
    username    = None # required for the abstract user
    
    USERNAME_FIELD  = "email" 
    # django authenticate with username and password but we will use email and password
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    # how user raw object will return 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"    