from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "seller", "title", "current_price")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "amount", "auction_listing")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commenter", "auction_listing")


# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.AuctionListing, AuctionListingAdmin)
admin.site.register(models.Bid, BidAdmin)
admin.site.register(models.Comment, CommentAdmin)
