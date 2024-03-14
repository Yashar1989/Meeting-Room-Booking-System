from django.contrib import admin
from .models import Room
from .models import Reservation

# Register your models here.
admin.site.register(Room)
admin.site.register(Reservation)
