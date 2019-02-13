from django import forms

from .models import *


class CartItemForm(forms.ModelForm):
    """Форма добавления товара"""
    class Meta:
        model = CartItem
        fields = ("quantity",)


class CommentForm(forms.ModelForm):
    """Форма добавления товара"""

    class Meta:
        model = Comment
        fields = ("text",)