from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.db import IntegrityError
from .models import Room, Reservation
from django.views.generic.edit import CreateView, View
from .forms import ReservationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from datetime import date
from comment.models import Comment


def UserCanCommit(request, room_no):
    room_id = Room.objects.get(room_no=room_no)
    reserved_list = Reservation.objects.filter(Q(user_id=request.user.id) & Q(room_id=room_id))
    if reserved_list:
        return True
    return False


class RoomListView(ListView):
    """
    Show rooms for all visitors
    """
    model = Room
    template_name = 'room/index.html'


class RoomDetailView(DetailView):
    """
    show room detail for all users
    """
    model = Room
    template_name = 'room/room_detail.html'
    slug_url_kwarg = 'room_no'
    slug_field = 'room_no'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(Q(reserve_id_id__room__room_no=self.kwargs['room_no']) & Q(parent=None))
        data['comments'] = comments
        data['can_comment'] = UserCanCommit(self.request, self.kwargs['room_no'])
        return data


def room_availability(request):
    """
    return available room for reserve
    """
    rooms = Room.objects.all()
    reservation = Reservation.objects.all()
    return render(request, 'room/room_availability.html', {'rooms': rooms, 'reservation': reservation})


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """
    view for create reserve
    only authenticated user can be create a reserve
    """
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
    """
    reservation list for user and admin
    """
    model = Reservation
    template_name = 'room/reserved_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(user=self.request.user)


class ActiveReserveView(LoginRequiredMixin, View):
    """
    activate reservation by admin
    """
    model = Reservation
    success_url = reverse_lazy('room:reserved-list')

    def get(self, request, *args, **kwargs):
        reserve = self.model.objects.get(id=kwargs.get('reserve_id'))
        reserve.is_active = True
        reserve.save()
        messages.success(request, 'رزرو با موفقیت تایید شد.')
        return redirect(self.success_url)


class DeleteReserve(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
    """
    delete reserve by admin
    """
    model = Reservation
    slug_url_kwarg = 'reserve_id'
    slug_field = 'id'
    success_url = reverse_lazy('room:reserved-list')
    success_message = 'رزرو مورد نظر با موفقیت حذف شد'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteReserve, self).delete(request, *args, **kwargs)
