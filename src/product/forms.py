from django import forms

# create forms


paginate_chices = (
    (8, "8"),
    (16, "16"),
    (24, "24"),
    (32, "32"),
)


class Paginate_by_form(forms.Form):
    pagination = forms.ChoiceField(
        label="نشان داده شود",
        choices=paginate_chices,
    )
