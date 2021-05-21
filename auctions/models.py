from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class ItemCategory(models.Model):
    categories = (
        ('Vehicles', 'Vehicles'),
        ('Sport', 'Sport'),
        ('Electronics', 'Electronics'),
        ('Accessories', 'Accessories'),
        ('Other', 'Others')
    )
    name = models.CharField(max_length=25, choices=categories)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_list')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    img = models.CharField(max_length=300, blank=True)
    start_bid = models.DecimalField(decimal_places=2, max_digits=9)
    current_bid = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True)
    winner = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.title}'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bid", blank=True)

    def __str__(self):
        return f'{self.user} bidded {self.item} for ${self.amount} @ {self.date}'


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField(max_length=300, blank=False)

    def __str__(self):
        return f'{self.item} - {self.comment} by {self.user}'


