# Generated by Django 5.0.2 on 2024-03-21 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_category_user_watch_list_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionlisting",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="auction_listing",
                to="auctions.category",
            ),
        ),
    ]
