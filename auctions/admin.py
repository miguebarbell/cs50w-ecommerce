from django.contrib import admin
from .models import User, Bid, Item, ItemCategory, Comment
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(ItemCategory)
admin.site.register(Comment)

# Register your models here.
