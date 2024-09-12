from django.contrib import admin
from .models import Doctor

# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('career', 'price')
    search_fields = ('career',)
    list_filter =('career',)


admin.site.register(Doctor,DoctorAdmin)    
