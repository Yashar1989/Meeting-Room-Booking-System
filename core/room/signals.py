# from .models import CustomUser, Profile
# from django.dispatch import receiver
# from django.db.models.signals import post_save

# @receiver(signal=post_save, sender=CustomUser)
# def save_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)