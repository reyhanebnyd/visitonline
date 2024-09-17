from django.contrib import admin
from .models import Appuser


@admin.register(Appuser)
class AppuserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "is_admin",
    ]
    list_filter = [
        "is_admin",
    ]
    actions = ['make_admin']
    @admin.action(description="Make selected users admin")
    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)
        self.message_user(request, f"{queryset.count()} users have been made admin.")
