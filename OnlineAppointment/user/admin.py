from django.contrib import admin
from .models import Appuser , Comment

# Register your models here.

@admin.register(Appuser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','is_admin')
    search_fields = ('username', 'email')
    


@admin.register(Comment)
class CommentAamin(admin.ModelAdmin):
    list_display = ('id_U','id_D','created')
    raw_id_fields = ('id_U','id_D')

