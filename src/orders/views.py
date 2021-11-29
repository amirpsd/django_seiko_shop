from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem

from suds.client import Client
from decouple import config


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


MERCHANT = config("MERCHANT")
client = Client("https://www.zarinpal.com/pg/services/WebGate/wsdl")
description = config("description")
mobile = config("mobile")
CallbackURL = "http://localhost:8000/orders/verify/"


@login_required
def payment(request, order_id, price):
    global amount, o_id
    amount = price
    o_id = order_id
    result = client.service.PaymentRequest(
        MERCHANT, amount, description, request.user.email, mobile, CallbackURL
    )
    if result.Status == 100:
        return redirect("https://www.zarinpal.com/pg/StartPay/" + str(result.Authority))
    else:
        return HttpResponse("Error code: " + str(result.Status))


@login_required
def verify(request):
    if request.GET.get("Status") == "OK":
        result = client.service.PaymentVerification(
            MERCHANT, request.GET["Authority"], amount
        )
        if result.Status == 100:
            order = Order.objects.get(id=o_id)
            order.paid = True
            order.save()
            messages.success(request, "Transaction was successful", "success")
            return redirect("shop:home")
        elif result.Status == 101:
            return HttpResponse("Transaction submitted")
        else:
            return HttpResponse("Transaction failed.")
    else:
        return HttpResponse("Transaction failed or canceled by user")
