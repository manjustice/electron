from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Category, Product, Order, Image


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("phone_number",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "phone_number",
                    )
                },
            ),
        )
    )


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Image)
