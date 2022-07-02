from django.utils.translation import gettext as _
from django import forms

# create forms


class CouponForm(forms.Form):
    code = forms.CharField(
        label=_("discount code"),
    )
