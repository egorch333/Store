from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View

from Store import settings

from .models import Profile
from .forms import ProfileForm


class ProfileDetail(LoginRequiredMixin, DetailView):
    """Вывод профиля пользователя"""
    model = Profile
    context_object_name = 'profile'
    template_name = 'profiles/profile_detail.html'


class ProfileUpdate(UpdateView):
    """Редактирование профиля"""
    form_class = ProfileForm
    model = Profile
    template_name = "profiles/profile_update.html"

    def form_valid(self, form):
        # return super().form_valid(form)
        print(form)

    def form_invalid(self, form):
        print(form.instance.country)
        print(form.instance.state)
        print(form.instance.city)
        return super().form_invalid(form)


# class ProfileAnonymUpdate(View):
#     """Редактирование профиля"""
#
#     def post(self, form):
#         anonym_key = self.request.POST.get('anonym_key')
#         pk = self.request.POST.get('pk')
#
#         # form = ProfileForm(self.request.POST)
#         # data = form.cleaned_data
#         data = self.request.POST.getlist
#         print('форма')
#         print(data)
#
#         return redirect("/checkout/{}/".format(pk))

class ProfileAnonymUpdate(View):
    """изменение данных пользователя"""
    def post(self, request):
        anonym_key = request.POST.get('anonym_key')
        pk = request.POST.get('pk')
        if(anonym_key is not None):
            """запись в бд"""
            form = ProfileForm(request.POST)

            """вытягиваю все данные формы"""
            data = {}
            data['phone'] = request.POST.get('phone')
            data['first_name'] = request.POST.get('first_name')
            data['state_id'] = request.POST.get('state')
            data['country_id'] = request.POST.get('country')
            data['city_id'] = request.POST.get('city')
            data['address'] = request.POST.get('address')
            data['last_name'] = request.POST.get('last_name')
            data['company_name'] = request.POST.get('company_name')
            data['anonym_key'] = request.POST.get('anonym_key')
            data['postcode'] = request.POST.get('postcode')

            if Profile.objects.filter(anonym_key=anonym_key).exists():
                Profile.objects.filter(anonym_key=anonym_key).update(**data)
            else:
                item = Profile(**data)
                item.save()

            messages.add_message(request, settings.MY_INFO, "Изменения внесены")
        else:
            messages.add_message(request, settings.MY_INFO, "Ошибка нет такого пользователя")

        return redirect("/checkout/{}/".format(pk))

