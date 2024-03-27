# Generated by Django 5.0.2 on 2024-03-26 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0012_rename_watch_list_user_watchlist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="auctionlisting",
            name="highest_bid",
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="bidding_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="current_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=8,
                validators=[django.core.validators.MinValueValidator(0.01)],
            ),
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="image",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                related_name="watchlist_user", to="auctions.auctionlisting"
            ),
        ),
    ]
