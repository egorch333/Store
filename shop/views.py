from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Product


class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/list-product.html"

class ProductView(DetailView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/detail-product.html"
    context_object_name = 'object_list'
    """
        Что я ни делаю ничего не выходит.
        только одно средство:
        self.kwargs['slug']
    """
    #slug_field = 'url'
    #slug_url_kwarg = 'url'
    # queryset = Product.objects.filter(slug='test1')

    def get_context_data(self, **kwargs):
        # расширяет функцию
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(slug=self.kwargs['slug'])
        return context
