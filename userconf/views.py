from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View


from Store import settings
from .models import *
from .form import *


class ProfileDetail(TemplateView):
    """Карточка товара"""
    model = Conf
    context_object_name = 'profile'
    template_name = 'userconf/profile.html'
    # form_class = CartItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context["profile"] = data = Conf.objects.get(user=self.request.user)
            """заполняю форму данными из базы instance, initial - для вставки простого словаря"""
            context["form"] = ConfForm(instance=data)
        except Conf.DoesNotExist:
            context["form"] = ''
        return context


class ProfileEdit(View):
    """изменение данных пользователя"""
    def post(self, request):
        user = request.user
        if(user is not None):
            """запись в бд"""
            form = ConfForm(request.POST)
            # check whether it's valid:
            """внутрення проверка формы"""
            if form.is_valid():
                """вытягиваю все данные формы"""
                data = form.cleaned_data

                try:
                    profile = Conf.objects.get(user=request.user)
                    Conf.objects.filter(user=request.user).update(**data)
                except Conf.DoesNotExist:
                    """добавляю пользователя"""
                    data["user"] = request.user
                    profile = Conf(**data)
                    profile.save()

                messages.add_message(request, settings.MY_INFO, "Изменения внесены")
            else:
                messages.add_message(request, settings.MY_INFO, "Ошибка при записи данных")
        else:
            messages.add_message(request, settings.MY_INFO, "Ошибка нет такого пользователя")
        return redirect("profile")