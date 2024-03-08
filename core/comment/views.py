from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from comment.forms import CommentForm


# Create your views here.
@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.author = request.user
            form.save()
    else:
        form = CommentForm()
    return render(request, 'comment/add_comment.html', {'form': form})
