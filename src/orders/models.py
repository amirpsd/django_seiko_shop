from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import User
from product.models import Product

from extensions.utils import jalali_convertor


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", verbose_name="کاربر"
    )
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

    def jalali_created(self):
        return jalali_convertor(self.created)

    jalali_created.short_description = "تاریخ ایجاد"

    def jalali_updated(self):
        return jalali_convertor(self.created)

    jalali_updated.short_description = "اخرین بروزرسانی"

    def __str__(self):
        return f"{self.user} - {str(self.id)}"

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total

    get_total_price.short_description = "مجموع خرید"


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
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    get_cost.short_description = "دریافت_هزینه"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name="کد تخفیف")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(verbose_name="اعتبار تا")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="تخفیف"
    )
    active = models.BooleanField(default=False, verbose_name="فغال")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"
