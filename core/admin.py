from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, User


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.unregister(User)


@admin.register(User)
class AuthUserAdmin(UserAdmin):
    search_fields = ["username", "get_full_name"]
    autocomplete_fields = ["groups", "user_permissions"]

    exclude = ["password"]
