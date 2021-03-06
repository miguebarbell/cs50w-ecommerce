# Generated by Django 3.1.7 on 2021-03-23 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210320_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='item',
            name='watchers',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.CharField(blank=True, help_text='URL of the image', max_length=300),
        ),
        migrations.AlterField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='name',
            field=models.CharField(choices=[('vehicles', 'Vehicles'), ('sport', 'Sport'), ('electronics', 'Electronics'), ('accessories', 'Accessories'), ('other', 'Others')], max_length=25),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
