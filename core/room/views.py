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
    return render(request, 'room/room_availability.html', {'rooms': rooms, 'reservation': reservation})


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
