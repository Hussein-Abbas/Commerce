from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class AuctionListing(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    starting_price = models.FloatField(null=False, blank=False)
    current_price = models.FloatField(null=False, blank=False)
    time = models.TimeField(auto_now_add=True, null=False, blank=False)
    bidding_count = models.IntegerField(default=0, null=False, blank=False)
    highest_bid = models.OneToOneField("Bid", on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.title} was selled by {self.seller}"


class Bid(models.Model):
    amount = models.IntegerField(null=False, blank=False)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=False, blank=False)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.amount}$ by {self.bidder}"


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=False, blank=False)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
