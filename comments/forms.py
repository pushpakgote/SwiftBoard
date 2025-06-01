from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    comment=forms.CharField(
        label=False,
        required=True,
        widget=forms.Textarea(attrs={'rows':3,'placeholder':"Enter Comment"})
        )

    class Meta:
        model = Comment
        fields = ['comment']

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters long")
        return comment
