from django.contrib import admin

from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "jalali_created",
        "jalali_updated",
        "address",
        "postal_code",
        "city",
        "paid",
    )
    list_filter = ("paid",)
    inlines = (OrderItemInline,)
