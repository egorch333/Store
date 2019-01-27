from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View


from .models import *
from .form import *


from django.http import HttpResponse

def home(request) :
    return HttpResponse("HelloWorld")
    # print('HelloWorld')


class ProfileDetail(TemplateView):
    """Карточка товара"""
    model = Conf
    context_object_name = 'profile'
    template_name = 'Profile/profile.html'
    # form_class = CartItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = data = Conf.objects.get(user=self.request.user)
        """заполняю форму данными из базы instance, initial - для вставки простого словаря"""
        context["form"] = ProfileForm(instance=data)
        return context


class ProfileEdit(View):
    """изменение данных пользователя"""
    def post(self, request):
        user = request.user
        if(user is not None):
            """запись в бд"""

            profile = Conf.objects.get(user=user)
            profile.phone = request.POST.get("phone", None)
            profile.company_name = request.POST.get("company_name", None)
            profile.payment_method = request.POST.get("payment_method", None)
            profile.first_name = request.POST.get("first_name", None)
            profile.last_name = request.POST.get("last_name", None)
            profile.address = request.POST.get("address", None)
            profile.email = request.POST.get("email", None)
            profile.save()
            messages.add_message(request, settings.MY_INFO, "Изменения внесены")
        else:
            messages.add_message(request, settings.MY_INFO, "Ошибка нет такого пользователя")
        return redirect("profile")