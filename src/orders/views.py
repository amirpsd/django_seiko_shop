from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem



@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            return render(request, "main/orders_created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "main/orders_create.html", {"cart": cart, "form": form})
