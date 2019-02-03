# Generated by Django 2.0.2 on 2019-02-02 09:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 2, 9, 18, 51, 342517, tzinfo=utc), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 2, 9, 18, 51, 347207, tzinfo=utc), verbose_name='Дата'),
        ),
    ]