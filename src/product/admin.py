from django.contrib import admin

from .models import (
    Product,
    Category,
    Color,
    Size,
    CategoryImage,
    Slider,
    Comment,
)


# Register your models here.
class CategoryImageInline(admin.TabularInline):
    model = CategoryImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "parent")
    list_filter = ("status", "title")
    search_fields = ("title", "slug")
    ordering = ("-parent", "title", "status")
    inlines = (CategoryImageInline,)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_html",
        "slug",
        "jpublish",
        "status",
        "is_new_product",
        "category_to_str",
    )
    list_filter = ("status", "publish")
    search_fields = ("title", "description", "slug")
    ordering = ["title"]
    list_per_page = 20


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "body", "created", "name")
    search_fields = ("user", "name")


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "image_html")


# register
admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Comment, CommentAdmin)
# admin action
# https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
