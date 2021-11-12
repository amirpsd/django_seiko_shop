from django.contrib.auth.models import AbstractUser
from django.db import models

from os.path import basename, splitext


def get_filename_ext(filepath):
    base_name = basename(filepath)
    name, ext = splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.username}{ext}"
    return f"users/{final_name}"


# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, null=True,
                                    verbose_name='تلفن همراه شما', default=None)
    image = models.ImageField(upload_to=upload_file_path, blank=True,
                              null=True,
                              verbose_name='تصویر',
                              help_text='برای پروفایل خود تصویر قرار دهید'
                              )
