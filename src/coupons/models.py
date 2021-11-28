from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name="کد تخفیف")
    valid_from = models.DateTimeField(verbose_name="اعتبار از")
    valid_to = models.DateTimeField(verbose_name="اعتبار تا")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="تخفیف"
    )
    active = models.BooleanField(default=False, verbose_name="فعال")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"
