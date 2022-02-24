from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.admin import display
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.db import models

from common.extensions.upload_file_path import upload_product_file
from common.extensions.code_generator import slug_generator
from common.extensions.decorators import format_image
from common.extensions.utils import jalali_convertor

from ckeditor_uploader.fields import RichTextUploadingField
from datetime import timedelta, datetime
import pytz

from .managers import ProductManager, CategoryManager

# Create your models here.


class CategoryImage(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, 
        default=None, verbose_name=_("category"),
    )
    title = models.CharField(
        max_length=150, verbose_name=_("title"),
    )
    images = models.FileField(
        upload_to=upload_product_file, verbose_name=_("image"),
    )

    def __str__(self):
        return self.category.title

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Category image")
        verbose_name_plural = _("Category images")


class Category(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        blank=True, default=None,
        null=True, related_name="children",
        verbose_name=_("subcategory"),
    )
    title = models.CharField(
        max_length=100, verbose_name=_("title"),
    )
    slug = models.SlugField(
        unique=True, null=False, 
        verbose_name=_("slug"),
    )
    status = models.BooleanField(
        default=False, verbose_name=_("to be displayed?"),
    )

    class Meta:
        verbose_name = _("Product category")
        verbose_name_plural = _("Products category")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product:category", args=[self.slug])

    objects = CategoryManager()


class Product(models.Model):
    STATUS_CHOICES = (
        ("a", _("available")),
        ("u", _("unavailable")),  
    )
    title = models.CharField(
        max_length=100, verbose_name=_("title"),
    )
    slug = models.SlugField(
        unique=True,  null=False,
        blank=True, verbose_name=_("slug"), 
    )
    price = models.PositiveIntegerField(
        default=0, blank=False,
        verbose_name=_("price"),
    )
    discount = models.IntegerField(
        default=0, blank=True,
        null=True, verbose_name=_("discount"),
    )
    description = RichTextUploadingField(
        default=None, blank=True,
        verbose_name=_("description"),
    )
    colors = models.ManyToManyField(
        "Color", related_name="products", 
        blank=True, verbose_name=_("colors"),
    )
    sizes = models.ManyToManyField(
        "Size", related_name="products",
        blank=True, verbose_name=_("Sizes"),
    )
    weight = models.CharField(
        max_length=80, default=None,
        verbose_name=_("Product weight"),
    )
    image_1 = models.ImageField(
        upload_to=upload_product_file, verbose_name=_("image 1"),
    )
    image_2 = models.ImageField(
        upload_to=upload_product_file, verbose_name=_("image 2"),
    )
    image_3 = models.ImageField(
        upload_to=upload_product_file, verbose_name=_("image 3"),
    )
    publish = models.DateTimeField(
        default=timezone.now, verbose_name=_("publication date"),
    )
    create = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    special_offer = models.BooleanField(
        default=False, verbose_name=_("special_offer"),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=1, 
        verbose_name=_("status"),
    )
    category = models.ManyToManyField(
        Category, related_name="products", 
        blank=True, verbose_name=_("categories"),
    )

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(slug_generator())
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @display(description=_("publication date"))
    def jpublish(self):
        return jalali_convertor(self.publish)

    @display(
        boolean=True,
        description=_("is new product?"),
    )
    def is_new_product(self):
        last_day = datetime.today() - timedelta(days=15)
        last_days = last_day.replace(tzinfo=pytz.timezone("UTC"))
        if self.publish >= last_days:
            return True
        else:
            return False

    @display(description=_("image"))
    @format_image
    def image_html(self):
        return (self.title, self.image_1.url)

    @display(description=_("categories"))
    def category_to_str(self):
        return " -- ".join([category.title for category in self.category.active()])

    @display(description=_("sizes"))
    def size_to_str(self):
        return " -- ".join([size.size for size in self.sizes.all()])

    @display(description=_("colors"))
    def color_to_str(self):
        return " -- ".join([color.color for color in self.colors.all()])

    def get_absolute_url(self):
        return reverse("product:detail", args=[self.slug, self.id])

    @property
    @display(description=_("The final price of the product with a discount"))
    def get_final_price(self):
        if self.discount:
            from math import ceil
            multiplier = self.discount / 100
            old_price = self.price
            new_price = ceil(old_price - (old_price * multiplier))
            return new_price
        else:
            return self.price

    objects = ProductManager()


class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name="comments", blank=False,
        null=False, verbose_name=_("user"),
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="comments", default=None,
        blank=False, null=False,
        verbose_name=_("product"),
    )
    name = models.CharField(
        max_length=60, verbose_name=_("name"),
    )
    body = models.TextField(
        max_length=500, verbose_name=_("body"),
    )
    created = models.DateField(default=timezone.now,)


    class Meta:
        ordering = ["-created", "-id"]
        unique_together = ("user", "created")
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.body


class Color(models.Model):
    color = models.CharField(
        max_length=50, unique=True,
        verbose_name=_("color"),
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = _("color")
        verbose_name_plural = _("colors")

    def __str__(self):
        return self.color


class Size(models.Model):
    size = models.CharField(
        max_length=3, unique=True,
        verbose_name=_("size"),
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = _("size")
        verbose_name_plural = _("sizes")

    def __str__(self):
        return self.size


class Slider(models.Model):
    title = models.CharField(
        max_length=100, blank=False, 
        verbose_name=_("title"),
    )
    image = models.ImageField(
        upload_to=upload_product_file, verbose_name=_("image"),
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
        verbose_name = _("slider")
        verbose_name_plural = _("sliders")


    @display(description="تصویر")
    @format_image
    def image_html(self):
        return (self.title, self.image.url)

