# Generated by Django 5.0.2 on 2024-03-21 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_alter_auctionlisting_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="auction_listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="auctions.auctionlisting",
            ),
        ),
    ]