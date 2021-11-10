from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

# Register your models here.
UserAdmin.list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff')

admin.site.register(User, UserAdmin)
