from .models import *
from django.shortcuts import render


def main():
    print("hello, world!")


def get_listing_id(request):
    try:
        return int(request.POST.get("listing_id"))
    except ValueError:
        message = "The listing id should be number!"
    except Exception:
        message = "Missing listing id"
    return render(request, "auctions/error.html", {
        "error_code": "400 bad request",
        "message": message
    }) 


def get_listing(request, listing_id):
    """if type(listing_id) is not int:
        return render(request, "auctions/error.html", {
            "error_code": "400 bad request",
            "message": "The listing id should be number!"
        })
    """
    try:
        return AuctionListing.objects.get(pk=listing_id, status=True)
    except Exception:
        return render(request, "auctions/error.html", {
                "error_code": "404 not found",
                "message": "You are trying to get an listing doesn't exit!",
        })


if __name__ == "__main__":
    main()

