from django.db import models


# Create your models here.

class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='نام'
    )
    email = models.EmailField(
        blank=False,
        verbose_name='ایمیل',
        unique=True,
        help_text='ایمیل نباید تکراری باشد',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'مخاطب'
        verbose_name_plural = 'مخاطبین'
