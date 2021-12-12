from django.contrib import messages
from django.contrib import admin

@admin.action(description="محصولات را منتشر کنید")
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status="pub")
    modeladmin.message_user(
        request, 
        f"{updated} محصول انتشار یافتند", 
        messages.SUCCESS,
    )

@admin.action(description="محصولات را از حالت انتشار خارج کنید")
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status="unp")
    modeladmin.message_user(
        request,
        f"{updated} محصول از حالت انشار خارج شد",
        messages.SUCCESS
    )