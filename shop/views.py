from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Sum
from django.db.models import Q

from Store import settings
from .models import *
from .form import *




class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    context_object_name = 'object_list'
    template_name = "shop/list-product.html"

    """
    не работает get что я ни делал )
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # context['object_list'] = Product.objects.all()
        return self.render_to_response(context)
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search", None)
        if search is not None:
            context['object_list'] = Product.objects.filter(Q(title__icontains=search) | Q(category__name__icontains=search))
        return context

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
        try:
            """принимаю товары в корзине - закрываю корзину"""
            cart = Cart.objects.get(user=request.user, accepted=False)
            cart.accepted = True
            cart.save()

            """создаю новую корзину"""
            Cart.objects.create(user=request.user, accepted=False)

            """создаю заказ"""
            order = Orders(
                cart=cart,
                accepted=True
            )
            messages.add_message(request, settings.MY_INFO, 'Создан заказ')
            order.save()
        except Cart.DoesNotExist:
            messages.add_message(request, settings.MY_INFO, 'Ваша корзина пуста!')
        return redirect("cart_item")



class OrderItemList(ListView):
    """Список всех заказов"""
    model = Orders
    template_name = "shop/list-orders.html"


