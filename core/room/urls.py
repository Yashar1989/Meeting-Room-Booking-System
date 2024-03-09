from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('' ,views.room_availability ,name='room_availability'),
]

