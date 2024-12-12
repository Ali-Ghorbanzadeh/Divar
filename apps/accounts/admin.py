from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class CustomUserAdmin(UserAdmin):
    ordering = ("id",)
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")})
    )


admin.site.register(UserProfile, CustomUserAdmin)
