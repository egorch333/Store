from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Product, Cart, CartItem, Order


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class CartAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['user', 'accepted']


class CartItemAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['product', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['cart', 'accepted']




admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)