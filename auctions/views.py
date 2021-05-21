from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ItemForm, CommentForm, BidForm
from .models import User, Item, Comment, ItemCategory, Bid


def index(request):
    items = Item.objects.all()
    return render(request, "auctions/index.html", {'items': items})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    items = Item.objects.all()
    form = ItemForm(data=request.POST)
    if request.method == 'POST' and form.is_valid():
        new = form.save(commit=False)
        new.user = request.user
        new.save()
        return render(request, "auctions/index.html", {'items': items})
    else:
        form = ItemForm()
    return render(request, "auctions/create.html", {'form': form})


def view_listing(request, item_id):
    item = Item.objects.get(id=item_id)
    watched = False
    price = max([item.start_bid, item.current_bid])
    comment_form = CommentForm()
    bid_form = BidForm()
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        watched = user in item.watchers.all()
    return render(request, "auctions/item.html", {
        'item': item, 'commentform': comment_form,
        'owner': request.user == item.user,
        'bidform': bid_form,
        'comments': Comment.objects.filter(item=item)[::-1],
        'watched': watched,
        'price': price,
        'won': str(request.user) == str(item.winner)
    })


@login_required
def action(request, item_id):
    global message
    item = Item.objects.get(id=item_id)
    price = max([item.start_bid, item.current_bid])
    comment_form = CommentForm(request.POST)
    bid_form = BidForm(request.POST)
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.item = item
            comment.user = request.user
            comment.save()
            message = f'Comment done for {item.title}'
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            if bid.amount > price:

                item.current_bid = bid.amount
                item.winner = str(request.user)
                print(item.winner)
                price = item.current_bid
                item.save()
                bid_model = Bid(user=user, amount=bid.amount, item=item)
                bid_model.save()
                message = f'You are the highest bidder for {item.current_bid}'
            else:
                message = f'Bid must be higher than {item.current_bid}'

    return render(request, "auctions/item.html", {
        'item': item, 'commentform': comment_form,
        'owner': request.user == item.user,
        'bidform': bid_form,
        'comments': Comment.objects.filter(item=item)[::-1],
        'message': message,
        'watched': item in Item.objects.filter(watchers=user),
        'price': price,
        'won': str(request.user) == str(item.winner)
    })


def categories(request):
    items = Item.objects.all()
    categories = ItemCategory.objects.all()
    for category in categories:
        print(category)
        for item in items:
            if item.category == category:
                print(item)

    return render(request, "auctions/categories.html", {
        'categories': categories, 'items': items
    })


@login_required
def watchlist(request):
    items = Item.objects.filter(watchers=request.user)
    print(f' items watched  {items}')
    return render(request, "auctions/watchlist.html", {
        'items': items
    })


@login_required
def close(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.user == item.user:
        item.status = False
        item.save()
    return redirect('item', item_id)


@login_required
def watch(request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(username=request.user)
    if user not in item.watchers.all():
        item.watchers.add(user)
        item.save()
    else:
        item.watchers.remove(user)
        item.save()
    return redirect('item', item_id)
