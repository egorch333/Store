from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Sum

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
        quantity = request.POST.get("quantity", None)
        if quantity is not None and int(quantity) > 0:
            try:
                item = CartItem.objects.get(cart__user=request.user, product_id=pk)
                item.quantity += int(quantity)
            except CartItem.DoesNotExist:
                item = CartItem(
                    cart=Cart.objects.get(user=request.user, accepted=False),
                    product_id=pk,
                    quantity=int(quantity)
                )
            item.save()
            messages.add_message(request, settings.MY_INFO, "Товар добавлен")
            return redirect("/detail/{}/".format(slug))
        else:
            messages.add_message(request, settings.MY_INFO, "Значение не может быть 0")
            return redirect("/detail/{}/".format(slug))


class CartItemList(ListView):
    """Товары в корзине подьзователя"""
    template_name = 'shop/cart.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)

    def get_context_data(self, **kwargs):
        """подсчёт суммы всех товаров в козине"""
        context = super().get_context_data(**kwargs)
        context['total'] = CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False).aggregate(Sum('price_sum'))
        return context


class EditCartItem(View):
    """Редактирование товара в карзине"""
    def post(self, request, pk):
        quantity = request.POST.get("quantity", None)
        if quantity:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.quantity = int(quantity)
            item.save()
        return redirect("cart_item")


class RemoveCartItem(View):
    """Удаление товара из корзины"""
    def get(self, request, pk):
        CartItem.objects.get(id=pk, cart__user=request.user).delete()
        messages.add_message(request, settings.MY_INFO, 'Товар удален')
        return redirect("cart_item")


class AddOrder(View):
    """Создание заказа"""
    def get(self, request):
        """принимаю товары"""
        cart = Cart.objects.get(user=request.user, accepted=False)
        cart.accepted = True
        cart.save()

        """создаю заказ"""
        try:
            order1 = Orders.objects.get(cart__user=request.user, cart__accepted=False)
            order1.cart = cart
            print(1)
            messages.add_message(request, settings.MY_INFO, 'Уже создан заказ')
        except Orders.DoesNotExist:
            print(2)
            messages.add_message(request, settings.MY_INFO, 'Создан заказ')
            # order1.save()

        return redirect("cart_item")
