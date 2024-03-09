from django.shortcuts import render
from .models import Room ,Reservation
from django.views.generic.edit import CreateView
from .models import Reservation
from .forms import ReservationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

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

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_Form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "The reservation was made successfully")
        return response

    def get_success_url(self):
        return reverse('')
