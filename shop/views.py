from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from Store import settings
from .models import *
from .form import *



class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/list-product.html"

class ProductDetail(DetailView):
    """Карточка товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product-detail.html'
    form_class = CartItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartItemForm()
        return context

class AddCartItem(View):
    """Добавление товара в карзину"""
    def post(self, request, slug, pk):
        form = CartItemForm(request.POST)
        if form.is_valid():

            # вытаскиваю цену продукта
            product = Product.objects.filter(id=pk)
            product = product.values('price')
            product = list(product)
            price = product[0]['price']
            price_sum = int(price) * int(request.POST['quantity'])

            # проверка на дублирование товара
            cart_obj = CartItem.objects.filter(product__id=pk)
            if len(cart_obj) > 0:
                # изменяю общую цену и количество (происходит сложение)
                cart = cart_obj.values('quantity')
                cart = list(cart)
                quantity = cart[0]['quantity'] + int(request.POST['quantity'])
                price_sum = int(price) * int(quantity)
                cart_obj.update(price_sum=price_sum, quantity=quantity)
            else:
                # добавляю общую цену и количество
                form = form.save(commit=False)
                form.product_id = pk
                form.cart = Cart.objects.get(user=request.user, accepted=False)
                form.price_sum = price_sum
                form.save()


            messages.add_message(request, settings.MY_INFO, "Товар добавлен")
            return redirect("/detail/{}/".format(slug))
        else:
            messages.add_message(request, settings.MY_INFO, "Error")
            return redirect("/detail/{}/".format(slug))


class CartItemList(ListView):
    template_name = 'shop/cart.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        arr_sum = CartItem.objects.values('price_sum')
        arr_sum = list(arr_sum)
        total = 0

        for value in arr_sum:
            print(value)
            total += value['price_sum']

        context["total"] = total
        return context


class CartItemEdit(View):
    """Редактирование товара в карзине"""
    def get(self, request, pk, price, quantity):
        print(pk, price, quantity)
        price_sum = price * quantity
        CartItem.objects.filter(id=pk).update(price_sum=price_sum, quantity=quantity)

        return redirect("/cart/")

class CartItemDell(View):
    """Редактирование товара в карзине"""
    def get(self, request, pk):
        CartItem.objects.filter(id=pk).delete()

        return redirect("/cart/")
