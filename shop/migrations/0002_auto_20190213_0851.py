# Generated by Django 2.0.2 on 2019-02-13 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 13, 8, 51, 1, 375023, tzinfo=utc), verbose_name='Дата'),
        ),
    ]
