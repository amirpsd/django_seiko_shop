from django import forms

# create forms


class CouponForm(forms.Form):
    code = forms.CharField(
        label="کد تخفیف",
    )
