from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from comment.forms import CommentForm


<<<<<<< HEAD
# Create your views here.
@login_required
def add_comment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author_id = request.user.id
                comment.save()
        else:
            return redirect(reverse('user:login'))
    else:
        form = CommentForm()
    return render(request, 'comment/add_comment.html', {'form': form})
=======
class RoomCommentsListView(ListView):
    model = Comment
    template_name = 'comment/comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        room_id = self.kwargs['pk']
        queryset = Comment.objects.filter(reserve_id__room_id=room_id)
        return queryset


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        reservation_id = self.kwargs['pk']
        reservation = Reservation.objects.get(pk=reservation_id)
        if reservation.user != self.request.user:
            raise Http404("You do not have permission to comment on this reservation.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        reservation_id = self.kwargs['pk']
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


class CommentDeleteView(LoginRequiredMixin, DeleteView):
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


class AdminCommentsView(TemplateView):
    template_name = 'comment/admin_comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inactive_comments'] = Comment.objects.filter(is_active=False)
        return context


class ActivateCommentsView(View):
    def post(self, request):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Only admin users can activate comments'}, status=403)
        comment_ids = request.POST.getlist('comments')
        Comment.objects.filter(pk__in=comment_ids).update(is_active=True)
        return redirect(reverse('admin_comments'))
>>>>>>> parent of bf15512 (Revert "Merge branch 'main' into bagher")
