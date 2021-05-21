from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("item/<int:item_id>", views.view_listing, name="item"),
    path("action/<int:item_id>", views.action, name="action"),
    path("close/<int:item_id>", views.close, name="close"),
    path("watch/<int:item_id>", views.watch, name="watch"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist")
]
