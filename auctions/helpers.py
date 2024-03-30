from .models import AuctionListing
from django.shortcuts import render


def main():
    print("hello, world!")


def get_listing_id(request):
    try:
        id = request.POST.get("listing_id")
        if id == None:
            message = "Missing listing ID."
        elif (id := int(id)) > 0:
            return id
        else:
            message = "Listing ID should be valid number."
    except Exception:
        message = "The listing ID should be a number."
    return render(request, "auctions/error.html", {
        "message": message
    }) 


def get_listing(request, listing_id, status=None):
    try:
        if status is not None:
            return AuctionListing.objects.get(pk=listing_id, status=status)
        return AuctionListing.objects.get(pk=listing_id)
    except Exception:
        return render(request, "auctions/error.html", {
            "message": "Database lookup error.",
        })


if __name__ == "__main__":
    main()

