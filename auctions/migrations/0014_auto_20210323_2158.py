# Generated by Django 3.1.7 on 2021-03-23 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20210323_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='watchers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]