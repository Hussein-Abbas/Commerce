from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("AuctionListing", related_name="watchlist_user")

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    image = models.URLField(blank=True)
    starting_price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, validators=[MinValueValidator(0.01)])
    current_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    bidding_count = models.IntegerField(default=0)
    seller = models.ForeignKey(User, related_name="auction_listing", on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, related_name="auction_listing", on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.title

    # Set current_price automaticly.
    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new instance
            self.current_price = self.starting_price
        super().save(*args, **kwargs)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, validators=[MinValueValidator(0.01)])
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=False)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return f"Bid of {self.amount}$ on {self.auction_listing}"


class Comment(models.Model):
    text = models.TextField(blank=False)
    auction_listing = models.ForeignKey(AuctionListing, related_name="comments", on_delete=models.CASCADE, blank=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.text
