from django import forms
from .models import Coupon
# create forms


class CouponForm(forms.Form):
    code = forms.CharField(
        label="کد تخفیف",
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        coupone = Coupon.objects.filter(code=code).exists()
        if coupone:
            raise forms.ValidationError("کد تخفیف مورد نظر موجود نیست")
        return code 