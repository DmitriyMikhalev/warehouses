from django.contrib.admin import ModelAdmin
from django.contrib import admin
from .models import Transit

@admin.register(Transit)
class TransitAdmin(ModelAdmin):
    list_display = ('id',)


