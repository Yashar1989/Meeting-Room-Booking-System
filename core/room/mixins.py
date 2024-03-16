from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Reservation


class SuperUserMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'شما دسترسی برای انجام این کار را ندارید')
            return redirect('room:index')


class OwnerOrSuperUser():
    def dispatch(self, request, reserve_id, *args, **kwargs):
        reserve = get_object_or_404(Reservation, id=reserve_id)
        if reserve.user == self.request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'شما دسترسی برای انجام این کار را ندارید')
            return redirect('room:index')