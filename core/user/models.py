from django.db import models
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField 
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here. 

class CustomUser(AbstractUser): 
    first_name = None 
    last_name = None 
    phone_number = PhoneNumberField(unique=True) 
    is_admin = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(signal=post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)