from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db import IntegrityError
from user.forms import CustomAuthenticationForm
from .models import Room, Reservation
from django.views.generic.edit import CreateView
from .models import Reservation
from .forms import ReservationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from datetime import date
from comment.models import Comment


class RoomListView(ListView):
    model = Room
    template_name = 'room/index.html'


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room/room_detail.html'
    slug_url_kwarg = 'room_no'
    slug_field = 'room_no'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(Q(reserve_id_id__room__room_no=self.kwargs['room_no']) & Q(is_active=True))
        data['comments'] = comments
        return data


def room_availability(request):
    rooms = Room.objects.all()
    reservation = Reservation.objects.all()
    return render(request, 'room/room_availability.html', {'rooms': rooms, 'reservation': reservation})


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'room/reservation_form.html'

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.room = Room.objects.get(room_no=self.kwargs.get('room_no'))
            response = super().form_valid(form)
            messages.success(self.request, "اتاق مورد نظر با موفقیت رزرو شد.")
            return response
        except IntegrityError:
            messages.error(self.request, 'اتاق مورد نظر در تاریخ و ساعت مشخص شده قبلاْ رزرو شده است.')
            print(self.kwargs.get('room_no'))
            return redirect(reverse('room:reservation_create', kwargs={'room_no': self.kwargs.get('room_no')}))

    def get_success_url(self):
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
