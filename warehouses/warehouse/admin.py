from django.contrib.admin import ModelAdmin
from django.contrib import admin
from .models import Transit, Owner, ProductTransit

@admin.register(Transit)
class TransitAdmin(ModelAdmin):
    list_display = ('id', 'date_start', 'date_end', 'warehouse')


@admin.register(ProductTransit)
class ProductTransitAdmin(ModelAdmin):
    list_display= ('id', 'transit', 'product', 'payload')


@admin.register(Owner)
class OwnerAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')