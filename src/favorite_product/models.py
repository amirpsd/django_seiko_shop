from django.db import models

from product.models import Product
from account.models import User


# Create your models here.


class FavoriteProduct(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        related_name="user_favorite_product",
    )
    products = models.ManyToManyField(
        Product, blank=False, default=None, related_name="products_favorite_product"
    )

    class Meta:
        verbose_name = "محصول مورد علاقه"
        verbose_name_plural = "محصولات مورد علاقه"

    def __str__(self):
        return self.user.username

    def product_to_str(self):
        return " -- ".join([product.title for product in self.products.all()])

    product_to_str.short_description = "محصولات"
