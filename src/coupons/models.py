from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(
        max_length=30, unique=True, 
        verbose_name=_("code"),
    )
    valid_from = models.DateTimeField(verbose_name=_("Credit from."),)
    valid_to = models.DateTimeField(verbose_name=_("Credit up."),)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_("discount"),
    )
    active = models.BooleanField(
        default=False, verbose_name=_("active"),
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("discount code")
        verbose_name_plural = _("discount codes")
