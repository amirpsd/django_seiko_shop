from django.contrib import admin

from .models import OrderItem, Order, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'jalali_created', 'jalali_updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline,)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)
