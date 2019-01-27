# -*- coding: utf-8 -*-
from django import forms
from .models import Conf



class ConfForm(forms.ModelForm):
    """Форма профиля пользователя"""

    class Meta:
        model = Conf
        fields = ("first_name","last_name","company_name","address","email","phone","payment_method")