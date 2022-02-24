from django.utils.translation import gettext as _
from django.db import models


# Create your models here.


class Contact(models.Model):
    name = models.CharField(
        max_length=100, blank=False, 
        verbose_name=_("name"),
    )
    email = models.EmailField(
        blank=False, unique=True,
        verbose_name=_("email"), help_text=_("Email should not be duplicate."),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
