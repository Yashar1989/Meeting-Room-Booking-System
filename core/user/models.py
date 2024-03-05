from django.db import models
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField 

# Create your models here. 

class CustomUser(AbstractUser): 
    first_name = None 
    last_name = None 
    phone_number = PhoneNumberField(unique=True) 
    is_admin = models.BooleanField(default=False)
