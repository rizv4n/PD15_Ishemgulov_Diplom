from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, CustomUserAdmin)
