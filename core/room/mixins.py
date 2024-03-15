from django.contrib import messages
from django.shortcuts import redirect


class SuperUserMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'شما دسترسی برای انجام این کار را ندارید')
            return redirect('room:index')