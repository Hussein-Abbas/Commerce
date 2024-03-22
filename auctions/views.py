from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    # Retrives all active listings.
    listings = AuctionListing.objects.filter(status=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


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


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "image", "starting_price", "category"]


def create_listing(request):
    """Create a new listing."""

    # When the method is POST.
    if request.method == "POST":
        # Retrives user-submitted data.
        form = CreateListingForm(request.POST)
        # Set the seller value
        form.instance.seller = request.user
        # Validate the form data.
        if form.is_valid():
            # If valid, save the new listing.
            form.save()
            # Redircet to the home page.
            return HttpResponseRedirect(reverse("index"))
        else:
            # If invalid, re-render the page with user inputs.
            return render(request, "auctions/create_listing.html", {
                "CreateListingForm": CreateListingForm(request.POST),
            })
    # When method is GET, render the page with empyt form for creating a new listing.
    return render(request, "auctions/create_listing.html", {
        "CreateListingForm": CreateListingForm(),
    })

@login_required(login_url="login")
def listing(request, listing_id):
    user = request.user
    listing = AuctionListing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": user.watchlist.filter(pk=listing_id),
        "comments": Comment.objects.filter(auction_listing=listing)
    })


@login_required(login_url="login")
def watchlist(request):
    user = request.user
    if request.method == "POST":
        listing_id = int(request.POST.get("listing_id"))
        listing = AuctionListing.objects.get(pk=listing_id)
        if request.POST.get("action") == "add":
            user.watchlist.add(listing)
            user.save()
        else:
            # Remov it
            user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        # Get the listing.
        listing = AuctionListing.objects.get(pk=int(request.POST.get("listing_id")))
        amount = float(request.POST.get("amount"))
        user = request.user
        if amount > listing.current_price:
            bid = Bid.objects.create(
                amount=amount,
                auction_listing=listing,
                bidder=user,
            )
            listing.current_price = amount
            listing.bidding_count += 1
            listing.highest_bid = bid
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=[request.POST.get("listing_id")]))
        else:
            return render(request, "auctions/error.html", {
                "error_code": "400 Bad request",
                "message": "The amount should be more than the current price!",
            })


@login_required(login_url="login")
def comment(request):
    if request.method == "POST":
        user = request.user
        text = request.POST.get("text")
        listing_id = int(request.POST.get("listing_id"))
        Comment.objects.create(
            text=text,
            auction_listing=AuctionListing.objects.get(pk=listing_id),
            bidder=user,
        )
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required(login_url="login")
def close(request):
    listing = AuctionListing.objects.get(pk=int(request.POST.get("listing_id")))
    seller = listing.seller
    if request.user == seller:
        listing.status = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/error", {
        "error_code": "403 Forbiden",
        "message": "You can't clse a listing that you don't selle it!"
    })