from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Comment
from room.models import Reservation


class CommentListView(ListView):
    model = Comment
    template_name = 'comment_list.html'
    context_object_name = 'comments'


class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment_detail.html'
    context_object_name = 'comment'


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        reservation_id = self.kwargs['reservation_id']
        reservation = Reservation.objects.get(pk=reservation_id)
        if reservation.user != self.request.user:
            raise Http404("You do not have permission to comment on this reservation.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        reservation_id = self.kwargs['reservation_id']
        reservation = Reservation.objects.get(pk=reservation_id)
        form.instance.reserve_id = reservation
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('room:index')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        reservation = self.object.reserve_id
        user = reservation.user
        if user != self.request.user:
            raise Http404("You do not have permission to edit this comment.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('room:index')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    success_url = reverse_lazy('comment_list')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.reserve_id.user
