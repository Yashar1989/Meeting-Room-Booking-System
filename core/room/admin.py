from django.contrib import admin
from .models import Room
from .models import Reservation

# Register your models here.
admin.site.register(Room)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'reserve_date', 'available_time', 'created_date', 'is_active')
    ordering = ('created_date', )