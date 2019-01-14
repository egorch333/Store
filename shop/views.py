from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .form import *
from django.views.generic.edit import FormMixin

from .models import Product



class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/list-product.html"

class ProductDetail(FormMixin, DetailView):
    """Карточка товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product-detail.html'
    form_class = CartItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

