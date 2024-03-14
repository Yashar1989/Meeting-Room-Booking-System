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
<<<<<<< HEAD
        return reverse('')
    return render(request ,'room/room_availability.html',{'rooms':rooms ,'reservation':reservation})
=======
        return reverse('room:index')

    def get_context_data(self, **kwargs):
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        context['free_time'] = Reservation.objects.filter(room__room_no=self.kwargs['room_no'],
                                                          reserve_date=date.today()).values('available_time', )
        context['room_no'] = self.kwargs.get('room_no')
        return context


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'room/reserved_list.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
>>>>>>> parent of bf15512 (Revert "Merge branch 'main' into bagher")
