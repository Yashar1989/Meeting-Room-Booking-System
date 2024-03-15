from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from room.models import Reservation
from django.contrib.messages.views import SuccessMessageMixin
from .models import Comment
from room.mixins import SuperUserMixin

def UserCanComment(request, *args, **kwargs):
    room_id = Reservation.objects.get(pk=kwargs['pk']).room_id
    reserved_list = Reservation.objects.filter(Q(room_id=room_id) & Q(user_id=request.user.id))
    if reserved_list:
        return True
    return False


class RoomCommentsListView(ListView):
    model = Comment
    template_name = 'comment/comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        room_id = self.kwargs['pk']
        queryset = Comment.objects.filter(reserve_id__room_id=room_id)
        return queryset


class CommentCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment/comment_form.html'
    success_url = reverse_lazy('room:index')
    success_message = 'نظر شما با موفقیت ثبت شد'

    def dispatch(self, request, *args, **kwargs):
        if UserCanComment(request, *args, **kwargs):
            if 'parent_id' in self.kwargs:
                self.parent_comment = get_object_or_404(Comment, pk=self.kwargs['parent_id'])
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You do not have permission to comment on this reservation.")

    def form_valid(self, form):
        if hasattr(self, 'parent_comment'):
            form.instance.reserve_id = self.parent_comment.reserve_id
            form.instance.parent = self.parent_comment
            form.instance.user_id = self.request.user
        else:
            form.instance.reserve_id = Reservation.objects.get(pk=self.kwargs['pk'])
            form.instance.user_id = self.request.user
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Comment, id=kwargs['pk'])

        reservation = self.object.reserve_id
        user = reservation.user
        if user != self.request.user:
            return render(request, 'index.html', context={'messages': ['you dont have permission']})

        if self.object.is_active:
            return render(request, 'comment/comment_form.html',
                          context={'messages': ['this comment was accepted, you cant edit']})
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('room:index')


class CommentDeleteView(LoginRequiredMixin, SuperUserMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs['pk'])
        reservation = comment.reserve_id
        user = reservation.user
        if user != self.request.user:
            raise Http404("You do not have permission to delete this comment.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('room:index')


class AdminCommentsView(SuperUserMixin, TemplateView):
    template_name = 'comment/admin_comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inactive_comments'] = Comment.objects.filter(is_active=False)
        return context


class ActivateCommentsView(SuperUserMixin, View):
    def post(self, request):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Only admin users can activate comments'}, status=403)
        comment_ids = request.POST.getlist('comments')
        Comment.objects.filter(pk__in=comment_ids).update(is_active=True)
        return redirect(reverse('comment:admin_comments'))
