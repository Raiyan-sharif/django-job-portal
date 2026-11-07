from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class PortalUserAdmin(UserAdmin):
    list_display = ('username', 'display_name', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type',)
    fieldsets = UserAdmin.fieldsets + (
        ('Portal', {'fields': ('display_name', 'user_type')}),
    )