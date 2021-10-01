from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, null=True,
                                    verbose_name='تلفن همراه شما', default=None)
