from django.contrib.admin.decorators import display
from django.contrib.admin import display
from django.db import models

from account.models import User
from product.models import Product, Color

from extensions.utils import jalali_convertor


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", verbose_name="کاربر"
    )
    full_name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    city = models.CharField(max_length=100, verbose_name="شهر")
    address = models.CharField(max_length=250, verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="پرداخت شده ؟")
    discount = models.IntegerField(
        blank=True, null=True, default=None, verbose_name="تخفیف"
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    @display(description="تاریخ ایجاد")
    def jalali_created(self):
        return jalali_convertor(self.created)

    @display(description="آخرین بروزرسانی")
    def jalali_updated(self):
        return jalali_convertor(self.created)

    def __str__(self):
        return f"{self.user} - {str(self.id)}"

    @display(description="مجموع خرید")
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="سفارش"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="محصول",
    )
    price = models.IntegerField(verbose_name="قیمت")
    color = models.ForeignKey(
        Color, 
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        default=None,
        verbose_name="رنگ", 
    )
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return str(self.id)

    @display(description="دریافت هزینه")
    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"
