from django.contrib import admin
from .models import FavoriteBlog


# Register your models here.
class FavoriteBlogAdmin(admin.ModelAdmin):
    list_display = ["__str__", "favorite_blog_to_str"]
    search_fields = ("user__username",)
    list_per_page = 30


admin.site.register(FavoriteBlog, FavoriteBlogAdmin)
