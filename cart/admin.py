from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'products', 'quantity', 'product_price']


admin.site.register(Cart, CartAdmin)
