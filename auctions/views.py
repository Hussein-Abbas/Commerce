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
    form = CreateListingForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.instance.seller = request.user
        form.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html", {
            "CreateListingForm": form,
    })


@login_required(login_url="login")
def listing(request, listing_id):
    # Validate and retrieve listing objcet.
    listing = get_listing(request, listing_id)
    if not isinstance(listing, AuctionListing):
      return listing 

    # Check if the listing is in the user's watchlist.
    in_watchlist = request.user.watchlist.filter(pk=listing_id).exists()

    # Get comments associated with the listing.
    comments = Comment.objects.filter(auction_listing=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "comments": comments
    })


@login_required(login_url="login")
def watchlist(request):
    user = request.user

    if request.method == "POST":
        # Get listing id and validtade it.
        listing_id = get_listing_id(request)
        if not isinstance(listing_id, int):
            return listing_id

        # Get listing and validate it.
        listing = get_listing(request, listing_id)
        if not isinstance(listing, AuctionListing):
            return listing

        # Get action to add or remove listing form watchlist.
        action = request.POST.get("action")

        # Add or remove watch list or render error.
        if action == "add":
            user.watchlist.add(listing)
        elif action == "remove":
            user.watchlist.remove(listing)
        else:
            return render(request, "auctions/error.html", {
                 "message": f"Invalid action",
            })

        # Redirect back to the same listing page.
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    # When the method is GET, display all active user listings.
    listings = user.watchlist.all() # Retrieve watchlist items.
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        user = request.user

        # Validate and retrieve the listing ID.
        listing_id = get_listing_id(request)
        if not isinstance(listing_id, int):
            return listing_id

        # Validate and retrieve the auction listing object.
        listing = get_listing(request, listing_id)
        if not isinstance(listing, AuctionListing):
            return listing

        # Validate and retrieve the bid amount.
        try:
            amount = float(request.POST.get("amount"))
            message = None
        except ValueError:
            message = "The amount should be a numebr!"

        # If an error message exists, render the error message.
        if message:
            return render(request, "auctions/error.html", {
                "message": message
            })

        # Ensure the bid amount is greater than the current price.
        if amount <= listing.current_price:
            return render(request, "auctions/error.html", {
                "message": f"The amount should be greater than ${listing.current_price}",
            })

        # Create a new bid.
        Bid.objects.create(amount=amount, auction_listing=listing, bidder=user)

        # Update the current price and bidding count of the listing.
        listing.current_price = amount
        listing.bidding_count += 1
        listing.save()

        # Redirect the user to the new listing page.
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    # If request method is GET, render error paeg 
    return render(request, "auctions/error.html", {
        "message": "Use the form to place a bid."
    })


@login_required(login_url="login")
def comment(request):
    if request.method == "POST":
        user = request.user

        # Validate and retrieve comment text.
        text = str(request.POST.get("text"))
        if not text:
            return render(request, "auctions/error.html", {
                "message": "Your comment must have text content."
            })

        # Validate and retrieve listing ID.
        listing_id = get_listing_id(request)
        if not isinstance(listing_id, int):
            return listing_id

        # Validate and retrieve listing.
        listing = get_listing(request, listing_id, status=True)
        if not isinstance(listing, AuctionListing):
            return listing

        # Create a new comment object.
        Comment.objects.create(text=text, commenter=user, auction_listing=listing)

        # Redircet the user to the same lising page.
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    # If request method is GET, render the error page.
    return render(request, "auctions/error.html", {
        "message": "Use form to place a comment."
    })


@login_required(login_url="login")
def close(request):
    if request.method == "POST":
        # Validate and retrieve the listing ID.
        listing_id = get_listing_id(request)
        if not isinstance(listing_id, int):
            return listing_id

        # Validate and retrieve the listing object.
        listing = get_listing(request, listing_id)
        if not isinstance(listing, AuctionListing):
            return listing

        # Validate if the user is the seller of this listing.
        listing_seller = listing.seller
        if request.user == listing_seller:
            listing.status = False

            # Remove the listing from any watchlist.
            listing.watchlist_user.clear()

            listing.save()

            # Redirect the user to home page.
            return HttpResponseRedirect(reverse("index"))

        return render(request, "auctions/error.html", {
                "message": "Only the seller of this listing can close it."
        })

    # If request method is GET, render the error page.
    return render(request, "auctions/error.html", {
        "message": "Use the form to close the listing."
    })


def category(request, category_id=None):
    # If category ID is provided in the URL.
    if category_id:
        # Validate and retrieve the category object.
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return render(request, "auctions/error.html", {
                "message": f"There is no category with ID {category_id}."
            })

        # Retrieve all active auction listings in this category.
        listings = AuctionListing.objects.filter(
            category=category, 
            status=True,
        )

        # Render the category page with its listings.
        return render(request, "auctions/category.html", {
                "listings": listings,
        })

    # If no category ID is provided, render the pgae with all categories.
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
            "categories": categories,
    })
