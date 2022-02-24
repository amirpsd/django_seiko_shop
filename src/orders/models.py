from django.contrib.admin.decorators import display
from django.utils.translation import gettext as _
from django.contrib.admin import display
from django.db import models

from product.models import Product, Color, Size
from account.models import User

from common.extensions.utils import jalali_convertor


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="orders", verbose_name=_("user"),
    )
    full_name = models.CharField(
        max_length=150, verbose_name=_("full name"),
    )
    city = models.CharField(
        max_length=100, verbose_name=_("city"),
    )
    address = models.CharField(
        max_length=250, verbose_name=_("address"),
    )
    postal_code = models.CharField(
        max_length=20, verbose_name=_("postal_code"),
    )
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    paid = models.BooleanField(
        default=False, verbose_name=_("is paid?"),
    )
    discount = models.IntegerField(
        blank=True, null=True, 
        default=None, verbose_name=_("discount"),
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    @display(description=_("the date of creation."))
    def jalali_created(self):
        return jalali_convertor(self.created)

    @display(description=_("last update."))
    def jalali_updated(self):
        return jalali_convertor(self.created)

    def __str__(self):
        return f"{self.user} - {str(self.id)}"

    @display(description=_("Total purchase."))
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, 
        related_name="items", verbose_name=_("order"),
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="order_items", verbose_name=_("product"),
    )
    price = models.IntegerField(verbose_name=_("price"),)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE,
        blank=False, null=False,
        default=None, verbose_name=_("color"), 
    )
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE,
        blank=False, null=False,
        default=None, verbose_name=_("size"), 
    )
    quantity = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("quantity"),
    )

    def __str__(self):
        return str(self.id)

    @display(description=_("get_cost"))
    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
