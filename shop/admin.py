from django.contrib import admin
from django import forms

from mptt.admin import MPTTModelAdmin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery

from .models import Category, Product, Cart, CartItem, Order




class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class CartAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['user', 'accepted']


class ProductAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['title', 'category', 'price', 'quantity']


class CartItemAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['cart', 'product', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['cart', 'accepted']


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['description']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)