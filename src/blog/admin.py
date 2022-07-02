from django.utils.translation import gettext as _
from django.contrib import admin

from .models import Blog, Category

# Register your models here.


admin.site.site_header = _("site management")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id", "slug", "parent", "status"]
    list_filter = ["status"]
    search_fields = ("title", "slug")
    fields = (
        "parent",
        ("title", "slug"),
        "status",
    )


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_html",
        "jpublish",
        "status",
        "category_to_str",
    )
    list_filter = ("publish", "status")
    search_fields = ("title", "slug", "id")
    radio_fields = {"status": admin.HORIZONTAL}
    filter_horizontal = ("category",)
    ordering = ("-status", "-create")
    exclude = ("slug",)
    list_per_page = 40


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
