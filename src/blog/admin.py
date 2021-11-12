from django.contrib import admin

from .models import Blog, Category

# Register your models here.


admin.site.site_header = 'مدیریت سایت'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'position', 'slug', 'parent', 'status']
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    ordering = (['status'])


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description', 'slug')
    ordering = ('-status', 'title', 'description')
    list_per_page = 20


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
