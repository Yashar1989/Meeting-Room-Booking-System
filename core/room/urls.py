from django.urls import path
from . import views



urlpatterns = [
    path('' ,views.room_availability ,name='room_availability'),
]
