from django.contrib.admin.decorators import display
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from django.db import models

from common.extensions.upload_file_path import upload_blog_file
from common.extensions.code_generator import slug_generator
from common.extensions.decorators import format_image
from common.extensions.utils import jalali_convertor

from ckeditor_uploader.fields import RichTextUploadingField

from .managers import BlogManager, CategoryManager


#################


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, 
        default=None, null=True, 
        blank=True, related_name="children",
        verbose_name=_("Subcategory"),
    )
    title = models.CharField(
        max_length=200, verbose_name=_("title"),
    )
    slug = models.SlugField(
        max_length=100, unique=True, 
        verbose_name=_("slug"),
    )
    status = models.BooleanField(
        default=False, verbose_name=_("status"),
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = _("blog category")
        verbose_name_plural = _("blogs category")

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Blog(models.Model):
    STATUS_CHOICES = (
        ("d", "draft"),
        ("p", "publish"),
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name="blogs", default=None,
        blank=False, null=False,
        verbose_name=_("author"),

    ) 
    title = models.CharField(
        max_length=200, verbose_name=_("title"),
    )
    slug = models.SlugField(
        max_length=100, unique=True, 
        blank=True, verbose_name=_("slug"),
    )
    category = models.ManyToManyField(
        Category, default=None,
        blank=False, related_name="blogs",
        verbose_name=_("categories"),
    )
    description = RichTextUploadingField(verbose_name=_("description"),)
    image = models.ImageField(
        upload_to=upload_blog_file, verbose_name=_("image"),
    )
    publish = models.DateTimeField(
        default=timezone.now, verbose_name=_("publication date"),
    )
    create = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True,)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES,
        verbose_name=_("status"),
    )

    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(slug_generator())
        super(Blog, self).save(*args, **kwargs)

    @display(description=_("publication date"))
    def jpublish(self):
        return jalali_convertor(self.publish)

    @display(description=_("image"))
    @format_image
    def image_html(self):
        return (self.title, self.image.url)

    @display(description=_("categories"))
    def category_to_str(self):
        return " -- ".join([category.title for category in self.category.active()])

    objects = BlogManager()
