from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from photologue.models import Gallery, Photo

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Категории товаров"""
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children')
    slug = models.SlugField(max_length=100, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Rating(models.Model):
    """Рейтинг товара"""
    # рейтинг
    rating_prod = models.IntegerField(default=0)
    q_vote = models.IntegerField(default=0)
    rating_result = models.IntegerField(default=0, help_text='рейтинг 0-5', verbose_name='рейтинг')
    date_create = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return "{}".format(self.rating_result)


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    price = models.IntegerField("Цена", default=0)
    slug = models.SlugField(max_length=150)
    availability = models.BooleanField("Наличие", default=True)
    quantity = models.IntegerField("Количество", default=0)
    photo = models.OneToOneField(
        Photo,
        verbose_name="Главная фотография",
        on_delete=models.SET_NULL,
        null=True)
    gallery = models.ForeignKey(
        Gallery,
        verbose_name="Фотографии",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    rating = models.OneToOneField(
        Rating,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class Cart(models.Model):
    """Корзина"""
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name='Принято к заказу', default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return "{}".format(self.user)


class CartItem(models.Model):
    """Товары в корзине"""
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price_sum = models.PositiveIntegerField("Общая сумма", default=0)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.price_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.cart)


class Order(models.Model):
    """Заказы"""
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name='Заказ выполнен', default=False)
    date = models.DateTimeField("Дата", default=timezone.now())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "{}".format(self.cart)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    text = models.TextField(blank=True, verbose_name='текст')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    # если нужно редактировать
    # create_date.editable=True
    change_date = models.DateTimeField(auto_now=True, verbose_name='время изменения')

    # для админки и shell
    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий к статье'
        verbose_name_plural = 'Комментарии к статье'
        ordering = ['-create_date']  # сортировка по умолчанию для всех страниц view


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Создание корзины пользователя"""
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=Product)
def create_vote_product(sender, instance, created, **kwargs):
    """рейтинг для товара"""
    if created:
        Product.objects.filter(id=instance.id).update(rating=instance.id)
        Rating.objects.create(id=instance.id)

