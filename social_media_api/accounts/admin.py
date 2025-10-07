from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'is_staff', 'is_active', 'bio',)
    list_filter = ('is_staff', 'is_active',)

    # Custom fieldsets for editing users
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_picture', 'followers')}),
    )

    # Fields for creating new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
