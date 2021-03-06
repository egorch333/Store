from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from Store import settings

from profiles.models import Profile
from profiles.forms import ProfileForm

from .models import *
from .forms import CartItemForm, CommentForm
from .serializers import ProductSer, CatSer


class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/list-product.html"
    paginate_by = 5


class ProductDetail(DetailView):
    """Карточка товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartItemForm()
        context["form_comment"] = CommentForm()
        context["user"] = self.request.user
        context["comments"] = Comment.objects.filter(product=context['product'].id)
        return context


class AddCartItem(View):
    """Добавление товара в карзину"""
    def post(self, request, slug, pk):
        quantity = request.POST.get("quantity", None)
        if quantity is not None and int(quantity) > 0:
            try:
                item = CartItem.objects.get(
                    cart__user=request.user,
                    product_id=pk,
                    cart__accepted=False)
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
    cart_items = ''

    def get_queryset(self):
        self.cart_items = CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)
        return self.cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_id"] = Cart.objects.get(user=self.request.user, accepted=False).id
        context["total"] = self.cart_items.aggregate(Sum('price_sum'))
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


class Search(View):
    """Поиск товаров"""
    def get(self, request):
        search = request.GET.get("search", None)
        products = Product.objects.filter(Q(title__icontains=search) |
                                          Q(category__name__icontains=search))

        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {"object_list": products, "page_obj": page_obj}

        return render(request, "shop/list-product.html", context)


class AddOrder(View):
    """Создание заказа"""
    def post(self, request):
        cart = Cart.objects.get(id=request.POST.get("pk"), user=request.user)
        cart.accepted = True
        cart.save()
        Order.objects.create(cart=cart)
        Cart.objects.create(user=request.user)
        return redirect('orders')


class OrderList(ListView):
    """Список заказов пользователя"""
    template_name = "shop/order-list.html"
    order = ''

    def get_queryset(self):
        self.order = Order.objects.filter(cart__user=self.request.user, accepted=False)
        return self.order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.order.aggregate(Sum('cart__cartitem__price_sum'))
        return context

    def post(self, request):
        """Удаление заказа"""
        order = Order.objects.get(id=request.POST.get("pk"), cart__user=request.user, accepted=False)
        Cart.objects.get(order__id=order.id, user=request.user, accepted=True).delete()
        order.delete()
        return redirect("orders")


class CheckOut(View):
    def get(self, request, pk):
        order = {}
        order['item'] = Order.objects.get(
            id=pk,
            cart__user=request.user,
            accepted=False
        )
        order['price'] = Order.objects.filter(
            id=pk,
            cart__user=request.user,
            accepted=False
        ).aggregate(Sum('cart__cartitem__price_sum'))
        form = ProfileForm(instance=Profile.objects.get(user=request.user))
        print(order)
        return render(request, 'shop/checkout.html', {"order": order, "form": form})


class CategoryProduct(ListView):
    """Список товаров из категории"""
    template_name = "shop/list-product.html"
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])
        return products


class CategoryProductVue(View):
    """Список товаров из категории для vue"""
    def get(self, request):
        return render(request, "shop/vue/list-product-vue.html")

    def post(self, request):
        slug = request.POST.get("slug")
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])

        category_ser = CatSer(Category.objects.filter(parent__isnull=True), many=True)
        serializers = ProductSer(products, many=True)
        return JsonResponse(
            {
                "products": serializers.data,
                "category": category_ser.data
            },
            safe=False)


class SortProducts(View):
    """Фильтр товаров"""
    def get(self, request):
        return render(request, "shop/vue/list-product-vue.html")

    def post(self, request):
        category = request.POST.get("category", None)
        price_1 = request.POST.get("price1", 1)
        price_2 = request.POST.get("price2", 1000000000)
        availability = request.POST.get("availability", None)

        filt = []

        if category:
            cat = Q()
            cat &= Q(category__name__icontains=category)
            filt.append(cat)
        if price_1 or price_2:
            price = Q()
            price &= Q(price__gte=int(price_1)) & Q(price__lte=int(price_2))
            filt.append(price)
        if availability:
            if availability == "False":
                avail = False
            elif availability == "True":
                avail = True
            availability = Q()
            availability &= Q(availability=avail)
            filt.append(availability)

        sort = Product.objects.filter(*filt)

        category_ser = CatSer(Category.objects.filter(parent__isnull=True), many=True)
        serializers = ProductSer(sort, many=True)
        return JsonResponse(
            {
                "products": serializers.data,
                "category": category_ser.data
             },
            safe=False)


class AddRatingProduct(View):
    """Рейтинг товаров"""

    def get(self, request, slug, rating):

        product = Product.objects.get(slug=slug)
        cur_rating = Rating.objects.get(pk=product.id)

        # новый рейтинг
        new_rating = cur_rating.rating_prod + int(rating)
        new_q_vote = cur_rating.q_vote + 1
        rating_result = new_rating / new_q_vote

        cur_rating.rating_result = int(rating_result)
        cur_rating.q_vote = new_q_vote
        cur_rating.rating_prod = new_rating
        cur_rating.save()

        messages.add_message(request, settings.MY_INFO, "Ваш рейтинг учтён!")
        return redirect("/detail/{}/".format(slug))


class AddCommentProduct(View):
    """Комментарии к товарам"""

    def post(self, request, pk, slug):
        text = request.POST.get('text', None)

        if text is not None:
            Comment.objects.create(product_id=int(pk), text=text, user=self.request.user)
        return redirect("/detail/{}/".format(slug))


class PayOrder(View):
    """оплата заказа по кнопке"""
    def get(self, request, pk):
        if self.request.user.is_authenticated:
            order = Order.objects.get(id=int(pk), cart__user=request.user)
        else:
            anonym_key = self.request.session['anonym_key']
            order = Order.objects.get(id=int(pk), cart__anonym_key=anonym_key,)
        order.accepted = True
        order.save()

        return redirect("/okpay-order/{}/".format(pk))


class OkPayOrder(DetailView):
    """Оплаченный заказ вывод"""
    model = Order
    context_object_name = 'order'
    template_name = 'shop/okpay-order.html'

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        order = Order.objects.filter(id=pk, cart__user=self.request.user, accepted=True)
        return order
