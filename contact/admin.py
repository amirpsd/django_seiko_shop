from django.contrib import admin

from .models import Contact


# Register your models here.

class NewslettersHomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    ordering = ('-id',)
    search_fields = ('email', 'name')
    list_per_page = 20


admin.site.register(Contact, NewslettersHomeAdmin)
