from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from product.models import Product

from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponForm


@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)  # create a new cart object passing it the request object
    product = get_object_or_404(Product, status='pub', id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        add_product_form  = form.cleaned_data
        cart.add(
            product=product, 
            color=add_product_form['color'], 
            quantity=add_product_form["quantity"], 
            update_quantity=add_product_form["override"],
        )
    return redirect("cart:cart_detail")


@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, status='pub', id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )

    coupon_apply_form = CouponForm()
    return render(request, "main/cart.html", {"cart": cart, 'coupon_apply_form': coupon_apply_form})
