from django.contrib import admin

from .models import FavoriteProduct


# Register your models here.
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_to_str']


admin.site.register(FavoriteProduct, FavoriteProductAdmin)
