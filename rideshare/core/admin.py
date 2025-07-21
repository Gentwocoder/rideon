from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DriverProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", "user_type")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    list_display = ("email", "is_staff", "is_active", "is_email_verified", "is_phone_verified")
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DriverProfile)