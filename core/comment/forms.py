from django import forms
from comment.models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reserve_id'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Reserve ID'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Comment'})

        for _, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Comment
        fields = ['reserve_id', 'comment']
