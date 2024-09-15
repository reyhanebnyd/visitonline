from django.contrib import admin
from .models import Appuser 

@admin.register(Appuser)
class AppuserAdmin(admin.ModelAdmin):
        list_display = [
            'id',
            'user',
            'is_admin',
        ]
        list_filter=[
                'is_admin',
        ]