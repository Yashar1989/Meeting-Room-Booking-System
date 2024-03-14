from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from comment.forms import CommentForm


# Create your views here.

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_id = request.user.id
            comment.save()
            return redirect(reverse('account:profile'))
    else:
        form = CommentForm()
    return render(request, 'comment/add_comment.html', {'form': form})
