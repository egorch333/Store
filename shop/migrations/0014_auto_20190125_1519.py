# Generated by Django 2.0.2 on 2019-01-25 15:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20190125_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 25, 15, 19, 32, 221168, tzinfo=utc), verbose_name='Дата'),
        ),
    ]
