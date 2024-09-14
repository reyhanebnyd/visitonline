from django import forms
from .models import Comments



class CommentForm (forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['context']
        widgets = {
            'context': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'write your comment ...'}),
        }    