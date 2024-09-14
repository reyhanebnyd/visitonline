from django.contrib import admin
from .models import Appuser , Comments

# Register your models here.

@admin.register(Appuser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('is_admin','user')

    


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_at',)


