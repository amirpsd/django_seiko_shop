from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib import admin

@admin.action(description=_("Make products available"))
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status="pub")
    modeladmin.message_user(
        request, 
        _(f"{updated} products were available"), 
        messages.SUCCESS,
    )

@admin.action(description=_("Make products unavailable"))
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status="unp")
    modeladmin.message_user(
        request,
        _(f"{updated} products were unavailable"),
        messages.SUCCESS
    )