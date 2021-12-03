from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from .models import Coupon
from .forms import CouponForm

# Create your views here.


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            messages.add_message(request, messages.ERROR, "کد تخفیف مورد نظر اشتباه است")
            request.session["coupon_id"] = None
    return redirect("cart:cart_detail")
