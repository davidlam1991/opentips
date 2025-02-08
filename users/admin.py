from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, OtpToken

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active")
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)


class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code", "verification_token")


admin.site.register(OtpToken, OtpTokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)