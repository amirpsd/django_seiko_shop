from django.contrib.admin.decorators import display
from django.db import models

from account.models import User
from blog.models import Blog


# Create your models here.


class FavoriteBlog(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_favoriteblogs", blank=False
    )
    blogs = models.ManyToManyField(Blog, related_name="blog_favoritblog", blank=False)

    class Meta:
        verbose_name = "مقاله مورد علاقه"
        verbose_name_plural = "مقالات مورد علاقه"

    def __str__(self):
        return self.user.get_full_name()

    @display(description="مقالات")
    def favorite_blog_to_str(self):
        return " -- ".join([blog.title for blog in self.blogs.all()])

