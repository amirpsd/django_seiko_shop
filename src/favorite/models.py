from django.contrib.admin.decorators import display
from django.utils.translation import gettext as _
from django.db import models

from product.models import Product
from account.models import User
from blog.models import Blog

# Create your models here.


class FavoriteProduct(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        unique=True, related_name="favorite_products",
    )
    products = models.ManyToManyField(
        Product, blank=False, 
        default=None, related_name="favorite_products",
    )

    class Meta:
        verbose_name = _("Favorite product")
        verbose_name_plural = _("Favorite products")

    def __str__(self):
        return self.user.username
    
    @display(description=_("products"))
    def product_to_str(self):
        return " -- ".join([product.title for product in self.products.all()])


class FavoriteBlog(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, 
        related_name="favorite_blogs", blank=False
    )
    blogs = models.ManyToManyField(
        Blog, related_name="favorite_blogs", 
        blank=False,
    )

    class Meta:
        verbose_name = _("Favorite blog")
        verbose_name_plural = _("Favorite blogs")

    def __str__(self):
        return self.user.get_full_name()

    @display(description=_("blogs"))
    def favorite_blog_to_str(self):
        return " -- ".join([blog.title for blog in self.blogs.all()])
