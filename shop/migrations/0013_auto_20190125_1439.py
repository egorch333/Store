# Generated by Django 2.0.2 on 2019-01-25 14:39

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0010_auto_20160105_1307'),
        ('shop', '0012_auto_20190124_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='photologue.Gallery', verbose_name='Фотографии'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 25, 14, 39, 11, 708374, tzinfo=utc), verbose_name='Дата'),
        ),
    ]
