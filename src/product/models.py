from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.db import models

from comment.models import Comment

from extensions.upload_file_path import upload_file_path
from extensions.code_generator import code_generator
from extensions.decorators import format_image
from extensions.utils import jalali_convertor

from ckeditor_uploader.fields import RichTextUploadingField
from datetime import timedelta, datetime
import pytz

from .managers import ProductManager, CategoryManager
#################

# Create your models here.


class CategoryImage(models.Model):
    category = models.ForeignKey(
        "Category", default=None, on_delete=models.CASCADE, verbose_name="دسته بندی"
    )
    title = models.CharField(max_length=150, verbose_name="عنوان")
    images = models.FileField(upload_to=upload_file_path, verbose_name="تصویر")

    def __str__(self):
        return self.category.title

    class Meta:
        ordering = ["-id"]
        verbose_name = "تصویر دسته بندی"
        verbose_name_plural = "تصویر دسته بندی ها"


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True,
        related_name="children",
        verbose_name="زیر دسته",
    )
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.SlugField(verbose_name="آدرس", null=False, unique=True)
    has_image = models.BooleanField(
        default=False, verbose_name="ایا مایل به انتشار تصویر هستید"
    )
    status = models.BooleanField(default=False, verbose_name="نمایش داده شود")

    class Meta:
        verbose_name = "دسته بندی محصول"
        verbose_name_plural = "دسته بندی محصولات"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product:category", args=[self.slug])

    objects = CategoryManager()


class Product(models.Model):
    STATUS_CHOICES = (
        ("pub", "منتشر شده"),  # publish
        ("unp", "منتشر نشده"),  # unpublish
    )
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.SlugField(verbose_name="آدرس", null=False, blank=True, unique=True)
    price = models.PositiveIntegerField(verbose_name="قیمت", default=0, blank=False)
    description = RichTextUploadingField(
        default=None, verbose_name="توضیحات", blank=True
    )
    color = models.ManyToManyField("Color", related_name="product_color", blank=True)
    size = models.ManyToManyField(
        "Size", verbose_name="سایز ها", related_name="product_size"
    )
    weight = models.CharField(max_length=200, verbose_name="ون محصول", default=None)
    image_1 = models.ImageField(upload_to=upload_file_path, verbose_name="تصویر 1")
    image_2 = models.ImageField(upload_to=upload_file_path, verbose_name="تصویر 2")
    image_3 = models.ImageField(upload_to=upload_file_path, verbose_name="تصویر 3")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    special_offer = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=3, verbose_name="وضعیت"
    )
    category = models.ManyToManyField(
        Category, related_name="category", blank=True, verbose_name="دسته بندی محصولات"
    )
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(code_generator())
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_convertor(self.publish)

    jpublish.short_description = "زمان انتشار"

    def is_new_product(self):
        last_day = datetime.today() - timedelta(days=15)
        last_days = last_day.replace(tzinfo=pytz.timezone("UTC"))
        if self.publish >= last_days:
            return True
        else:
            return False

    is_new_product.short_description = "وضعیت جدید بودن"
    is_new_product.boolean = True

    @format_image
    def image_html(self):
        return (self.title, self.image_1.url)

    image_html.short_description = "تصویر"

    def category_to_str(self):
        return " -- ".join([category.title for category in self.category.active()])

    category_to_str.short_description = "دسته بندی ها"

    def size_to_str(self):
        return " -- ".join([size.size for size in self.size.all()])

    size_to_str.short_description = "سایز ها"

    def color_to_str(self):
        return " -- ".join([color.color for color in self.color.all()])

    size_to_str.short_description = "رنگ ها"

    def get_absolute_url(self):
        return reverse("product:detail", args=[self.slug, self.id])

    objects = ProductManager()


class Color(models.Model):
    color = models.CharField(max_length=50, verbose_name="رنگ", unique=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"

    def __str__(self):
        return self.color


class Size(models.Model):
    size = models.CharField(max_length=3, verbose_name="سایز", unique=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "سایز"
        verbose_name_plural = "سایز ها"

    def __str__(self):
        return self.size


class Slider(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name="عنوان")
    image = models.ImageField(upload_to=upload_file_path, verbose_name="تصویر")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"

    @format_image
    def image_html(self):
        return (self.title, self.image.url)

    image_html.short_description = "تصویر"
