# Generated by Django 3.1.7 on 2021-03-23 21:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210323_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='watchers',
        ),
        migrations.AddField(
            model_name='item',
            name='watchers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
