from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

    def form_valid(self, form):
        form.instance.user = self.request.user

        reservation_id = self.kwargs['reservation_id']
        reservation = Reservation.objects.get(pk=reservation_id)
        form.instance.reserve_id = reservation

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('comment_list_view')

    def get_queryset(self):
        return super().get_queryset().filter(reserve_id__user=self.request.user)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'comment_create.html.html'
    fields = ['comment']
    context_object_name = 'comment'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.reserve_id.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    success_url = reverse_lazy('comment_list')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.reserve_id.user
