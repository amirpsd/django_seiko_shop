from django.contrib.admin.decorators import display
from django.utils.text import slugify
from django.utils import timezone
from django.db import models

from extensions.upload_file_path import upload_file_path
from extensions.code_generator import code_generator
from extensions.decorators import format_image
from extensions.utils import jalali_convertor

from ckeditor_uploader.fields import RichTextUploadingField

from .managers import BlogManager, CategoryManager


#################


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="زیر دسته",
    )
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته بندی ")
    status = models.BooleanField(default=False, verbose_name="آیا نمایش داده شود")
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی مقاله"
        verbose_name_plural = "دسته بندی مقالات"
        ordering = ["parent__id", "position"]

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Blog(models.Model):
    STATUS_CHOICES = (
        ("d", "پیش نویس"),
        ("p", "منتشر شده"),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name="آدرس", blank=True
    )
    category = models.ManyToManyField(
        Category,
        default=None,
        blank=False,
        verbose_name="دسته بندی",
        related_name="blogs",
    )
    description = RichTextUploadingField(verbose_name="توضیحات")
    image = models.ImageField(upload_to=upload_file_path, verbose_name="تصویر")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت"
    )

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(code_generator())
        super(Blog, self).save(*args, **kwargs)

    @display(description="تاریخ انتشار")
    def jpublish(self):
        return jalali_convertor(self.publish)

    @display(description="تصویر")
    @format_image
    def image_html(self):
        return (self.title, self.image.url)

    @display(description="دسته بندی")
    def category_to_str(self):
        return " -- ".join([category.title for category in self.category.active()])

    objects = BlogManager()
