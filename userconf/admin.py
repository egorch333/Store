from django.contrib import admin

from .models import Conf



class ConfAdmin(admin.ModelAdmin):
    # вывод названия в таблице
    list_display = ['first_name', 'last_name', 'phone', 'email']

admin.site.register(Conf, ConfAdmin)