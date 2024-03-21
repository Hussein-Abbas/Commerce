from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *


def index(request):
    return render(request, "auctions/index.html")


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
        fields = ["title", "description", "image", "starting_price", 
                  "seller", "category"]


def create_listing(request):
    """Create new listing."""

    # When the method is POST.
    if request.method == "POST":
        # Retrives user-submitted data.
        form = CreateListingForm(request.POST)
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