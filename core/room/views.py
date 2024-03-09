from django.shortcuts import render
from .models import Room ,Reservation
# Create your views here.

def room_availability(request):
    rooms = Room.objects.all()
    reservation = Reservation.objects.all()
    return render(request ,'room/room_availability.html',{'rooms':rooms ,'reservation':reservation})
