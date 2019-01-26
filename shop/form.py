# -*- coding: utf-8 -*-
from django import forms
from .models import CartItem, Profile

# class CartItemForm(forms.Form):
#     error_css_class = 'error'
#     required_css_class = 'required'
#
#     quantity = forms.CharField(
#         label='',
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control input-number',
#                                       'required': True,
#                                       'id': 'quantity',
#                                       'name': 'quantity',
#                                         'value': '1',
#                                         'min': '1',
#                                         'max': '100'}),
#     )

class CartItemForm(forms.ModelForm):
    """Форма добавления товара"""

    class Meta:
        model = CartItem
        fields = ("quantity",)


class ProfileForm(forms.ModelForm):
    """Форма профиля пользователя"""

    class Meta:
        model = Profile
        fields = ("first_name","last_name","company_name","address","email","phone","payment_method")