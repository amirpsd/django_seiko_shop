from django.contrib import admin

from .models import FavoriteProduct, FavoriteBlog 


# Register your models here.

class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "product_to_str"]

admin.site.register(FavoriteProduct, FavoriteProductAdmin)


class FavoriteBlogAdmin(admin.ModelAdmin):
    list_display = ["__str__", "favorite_blog_to_str"]
    search_fields = ("user__username",)
    list_per_page = 30

admin.site.register(FavoriteBlog, FavoriteBlogAdmin)
