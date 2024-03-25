from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .helpers import *
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
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
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
    listing = get_listing(request, listing_id)
    if type(listing) is not AuctionListing:
      return listing

    return render(request, "auctions/listing.html", {
            "listing": listing,
            "in_watchlist": user.watchlist.filter(pk=listing_id),
            "comments": Comment.objects.filter(auction_listing=listing),
        })


@login_required(login_url="login")
def watchlist(request):
    user = request.user
    if request.method == "POST":
        # Get listing id
        listing_id = get_listing_id(request)
        # Validtade it
        if not isinstance(listing_id, int):
            return listing_id
        # Get listing.
        listing = get_listing(request, listing_id)
        # Validate it.
        if not isinstance(listing, AuctionListing):
            return listing
        # Get action to add or remove listing form watchlist.
        try:
            action = request.POST.get("action")
        except Exception:
            return render(request, "auctions/error.html", {
                "error_code": "400 bad request",
                "message": "There isn't any action!"
            })
        # Validate action.
        if action == "add":
            # Add listing to watchlist.
            user.watchlist.add(listing)
            # Save the user.
            user.save()
        elif action == "remove":
            # Remove it.
            user.watchlist.remove(listing)
        # If action isn't add or remove, render error page.
        else:
            return render(request, "auctions/error.html", {
                    "error_code": "400 bad request",
                    "message": f"We dont' support {action} action!",
            })
        # Display to the user the same listing page.
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    # When the method is GET, display all active user listings.
    return render(request, "auctions/watchlist.html", {
        "listings": user.watchlist.filter(status=True)
    })


@login_required(login_url="login")
def bid(request):
    # When user submit form.
    if request.method == "POST":
        # Get user.
        user = request.user
        # Get listing id and validate it.
        listing_id = get_listing_id(request)
        if not isinstance(listing_id, int):
            return listing_id
        # Get the listing and validate it.
        listing = get_listing(request, listing_id)
        if not isinstance(listing, AuctionListing):
            return listing
        # Get amount 
        try:
            amount = float(request.POST.get("amount"))
            message = None
        except ValueError:
            message = "The amount should be numebr"
        except Exception:
            message = "There isn't amount!"
        # If message has value, return error code with message.
        if message:
            return render(request, "auctions/error.html", {
                "error_code": "400 bad request",
                "message": message
            })
        # Validate amount greater than current price.
        if amount > listing.current_price:
            # Create new bid.
            bid = Bid.objects.create(
                amount=amount,
                auction_listing=listing,
                bidder=user,
            )
            # Set the values of the new listing.
            listing.current_price = amount
            listing.bidding_count += 1
            listing.highest_bid = bid
            # Save the new listing
            listing.save()
            # Redirect user to the new listing page
            return HttpResponseRedirect(
                reverse("listing", args=[listing_id])
            )
        # If amount isn't greater than current price, render error page.
        else:
            return render(request, "auctions/error.html", {
                    "error_code": "400 Bad request",
                    "message": "The amount should be more than the current price!",
            })


@login_required(login_url="login")
def comment(request):
    if request.method == "POST":
        # Get user.
        user = request.user
        # Get the content of comment.
        text = request.POST.get("text")
        # Get listing id and validate it
        listing_id = get_listing_id(request)
        if not isinstance(listing_id, int):
            return listing_id

        Comment.objects.create(
            text=text,
            auction_listing=AuctionListing.objects.get(pk=listing_id),
            bidder=user,
        )
        # Redircet user to the same lising page
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required(login_url="login")
def close(request):
    listing = get_listing(request, get_listing_id(request))
    if not isinstance(listing, AuctionListing):
        return listing

    seller = listing.seller
    if request.user == seller:
        listing.status = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/error.html", {
            "error_code": "403 Forbiden",
            "message": "You can't close a listing that you don't sell it!",
        })


def category(request, category_id=None):
    if category_id:
        category = Category.objects.get(pk=category_id)
        listings = AuctionListing.objects.filter(category=category, status=True)
        return render(request, "auctions/category.html", {
                "listings": listings,
        })
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
            "categories": categories,
        })
