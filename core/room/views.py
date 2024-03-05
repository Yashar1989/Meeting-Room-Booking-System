from django.shortcuts import render
from .models import Room ,Reservation
# Create your views here.

def room_availability(request):
    rooms = Room.objects.all()
    reservation = Reservation.objects.all()
    free_room = {}
    reserve_room = {}
    for room in rooms:
        for reserve in reservation:
            if room.id == reserve.room_id.id:
                if reserve.start_time and reserve.end_time:
                    reserve_start_time = reserve.start_time
                    reserve_end_time = reserve.end_time
                    if room.room_no not in reserve_room:
                        reserve_room[room.room_no] = []
                    reserve_room[room.room_no].append((reserve_start_time,reserve_end_time))
                else:
                    reserve_start_time = reserve.start_time
                    reserve_end_time = reserve.end_time
                    if room.room_no not in free_room:
                        free_room[room.room_no] = []
                    free_room[room.room_no].append((reserve_start_time,reserve_start_time))
    return render(request ,'room_availability.html',{'free_room':free_room ,'reserve_room':reserve_room})