from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, otp=None ,**kwargs):
        try:
            user = User.objects.get(email=email)
            if user.stored_otp == otp:
                return user
        except User.DoesNotExist:
            return None
        
# class PhoneAuthBackend:
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(phone_number=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except (User.DoesNotExist, User.MultipleObjectsReturned):
#             return None
        
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
