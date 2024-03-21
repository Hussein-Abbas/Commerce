from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watch_list = models.ManyToManyField(
        "AuctionListing", null=True, blank=True, related_name="watchlist_user"
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    starting_price = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    bidding_count = models.IntegerField(default=0, null=False, blank=False)
    highest_bid = models.OneToOneField(
        "Bid", on_delete=models.SET_NULL, null=True, blank=True
    )
    seller = models.ForeignKey(
        User,
        related_name="auction_listing",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        related_name="auction_listing",
        on_delete=models.SET_DEFAULT,
        default=1,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.title} was sold by {self.seller}"

    # Set current_price automaticly.
    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new instance
            self.current_price = self.starting_price
        super(AuctionListing, self).save(*args, **kwargs)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, null=False, blank=False
    )
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.amount}$ by {self.bidder}"


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    auction_listing = models.ForeignKey(
        AuctionListing, related_name="comments",on_delete=models.CASCADE, null=False, blank=False
    )
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
