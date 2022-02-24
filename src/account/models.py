from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models

from common.extensions.upload_file_path import upload_user_file


# Create your models here.


class User(AbstractUser):
    image = models.ImageField(
        upload_to=upload_user_file, blank=True,
        null=True, verbose_name=_("image"),
        help_text=_("Put a picture for your profile"),
    )
