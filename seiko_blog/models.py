from django.contrib.contenttypes.fields import GenericRelation
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils import timezone
from django.db import models

from extensions.upload_file_path import upload_file_path
from extensions.code_generator import code_generator
from extensions.utils import jalali_convertor

from comment.models import Comment
from ckeditor_uploader.fields import RichTextUploadingField

from .managers import BlogManager, CategoryManager

#################


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name='آدرس دسته بندی ')
    status = models.BooleanField(
        default=False, verbose_name='آیا نمایش داده شود')
    position = models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی مقالات'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Blog(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name='آدرس', blank=True)
    category = models.ManyToManyField(Category, default=None, blank=False, verbose_name='دسته بندی',
                                      related_name="blog_category")
    description = RichTextUploadingField(verbose_name='توضیحات')
    image = models.ImageField(upload_to=upload_file_path, verbose_name='تصویر')
    publish = models.DateTimeField(
        default=timezone.now, verbose_name='زمان انتشار')
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(code_generator())
        super(Blog, self).save(*args, **kwargs)

    def jpublish(self):
        return jalali_convertor(self.publish)

    jpublish.short_description = "تاریخ انتشار"

    def image_tag(self):
        return format_html(f'<img style="border-radius: 5px;" width=100 height=60 src="{self.image.url}">')

    image_tag.short_description = 'عکس'

    def category_to_str(self):
        return " -- ".join([category.title for category in self.category.active()])

    category_to_str.short_description = "دسته بندی"

    objects = BlogManager()
