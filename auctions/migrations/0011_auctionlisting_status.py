# Generated by Django 5.0.2 on 2024-03-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_rename_img_auctionlisting_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
