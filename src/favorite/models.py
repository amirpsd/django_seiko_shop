from django.contrib.admin.decorators import display
from django.db import models

from product.models import Product
from account.models import User
from blog.models import Blog

# Create your models here.


class FavoriteProduct(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        related_name="favorite_products",
    )
    products = models.ManyToManyField(
        Product, blank=False, default=None, related_name="favorite_products"
    )

    class Meta:
        verbose_name = "محصول مورد علاقه"
        verbose_name_plural = "محصولات مورد علاقه"

    def __str__(self):
        return self.user.username
    
    @display(description="محصولات")
    def product_to_str(self):
        return " -- ".join([product.title for product in self.products.all()])


class FavoriteBlog(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="favorite_blogs", blank=False
    )
    blogs = models.ManyToManyField(Blog, related_name="favorite_blogs", blank=False)

    class Meta:
        verbose_name = "مقاله مورد علاقه"
        verbose_name_plural = "مقالات مورد علاقه"

    def __str__(self):
        return self.user.get_full_name()

    @display(description="مقالات")
    def favorite_blog_to_str(self):
        return " -- ".join([blog.title for blog in self.blogs.all()])
