from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Conf(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    company_name = models.CharField("Компания", max_length=100, null=True, blank=True,)
    address = models.CharField("Адрес", max_length=100, null=True, blank=True,)
    email = models.CharField("Email", max_length=100)
    phone = models.CharField("Телефон", max_length=50, null=True, blank=True,)

    PAYMENT_CHOICES = (
        ('Direct Bank Tranfer', 'Direct Bank Tranfer'),
        ('Check Payment', 'Check Payment'),
        ('Paypal', 'Paypal'),
    )

    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты', default='Direct Bank Tranfer')
    date = models.DateTimeField("Дата", default=timezone.now())

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return "{}".format(self.first_name)