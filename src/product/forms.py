from django.utils.translation import gettext as _
from django import forms

from .models import Comment

# Create your forms here.


class Paginate_by_form(forms.Form):
    paginate_choice = (
        (8, "8"),
        (16, "16"),
        (24, "24"),
        (32, "32"),
    )
    pagination = forms.ChoiceField(
        label=_("be shown"),
        choices=paginate_choice,
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "body")
