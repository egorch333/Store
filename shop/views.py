from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .form import *
from django.views.generic.edit import FormMixin

from .models import *
from django.contrib.auth.models import User
from django.db import IntegrityError



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

        """записываю данные в БД"""
        if(self.request.GET):
            quantity = self.request.GET['quantity']
            slug = self.kwargs['slug']
            # users = User.objects.values()
            # cur_user = users[0].get('username')
            # user = str(self.request.user)
            # print(type(str(self.request.user)))
            try:
                cart = Cart.objects.create(user=self.request.user)
                print(1)
            except IntegrityError:
                cart = Cart.objects.filter(user=self.request.user)[0]
                print(cart)

            product = Product.objects.filter(slug=slug)[0]
            # product_id = Product.objects.filter(slug=slug)[0].id
            CartItem.objects.create(product=product, quantity=quantity, cart=cart)

            check_cart = Orders.objects.filter(cart=cart)
            # Orders.objects.filter(id=1)[0].id
            if len(check_cart) == 0:
                Orders.objects.create(cart=cart)

        return context