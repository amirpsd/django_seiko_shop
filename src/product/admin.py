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
from .actions import make_draft, make_published

# Register your models here.
class CategoryImageInline(admin.TabularInline):
    model = CategoryImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "parent")
    list_filter = ("status", "title")
    search_fields = ("title", "slug", "id")

    ordering = ("status", "-id",)
    inlines = (CategoryImageInline,)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_html",
        "jpublish",
        "status",
        "is_new_product",
        "category_to_str",
        "price",
        "get_final_price",
    )
    list_filter = ("status", "special_offer")
    search_fields = ("title", "slug", "id")
    radio_fields = {"status": admin.HORIZONTAL}
    filter_horizontal = ["category", "colors", "sizes"]
    ordering = ["-create", "-updated"]
    actions = (make_published, make_draft)
    exclude = ("slug",)
    list_per_page = 40


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
