from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('bio', 'website', 'profile_image')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'follower_count']
