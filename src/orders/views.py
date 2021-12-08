from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order

from xhtml2pdf import pisa


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
                print("*"*30)
                print(item["color"])
                print("*"*30)
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    color_id=item["color_id"],
                    size_id=item["size_id"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            return render(request, "main/orders_created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "main/orders_create.html", {"cart": cart, "form": form})


@login_required
def render_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    template_path = "main/pdf.html"
    context = {
        "order": order,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")

    # if download
    # response['Content-Disposition'] = f'attachment; filename="{order.id}{order.user.username}.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
    )
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response
