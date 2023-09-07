from django.db import models
import datetime
from item_db.models import Item
from django.utils import timezone


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=50)
    expires_in = models.PositiveIntegerField()  # in seconds
    timestamp = models.DateTimeField(auto_now_add=True)  # when the token was stored

    @property
    def is_valid(self):
        """Check if token is still valid"""
        token_age = timezone.now() - self.timestamp
        return token_age < datetime.timedelta(seconds=self.expires_in)


class Auction(models.Model):
    auction_id = models.BigIntegerField(primary_key=True, verbose_name="Auction ID")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    bid = models.PositiveIntegerField(verbose_name="Bid Amount")
    buyout = models.PositiveIntegerField(verbose_name="Buyout Amount")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    time_left = models.CharField(max_length=50, verbose_name="Time Left")

    # Capture the timestamp of when the record is created. (When we make API call)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"
        ordering = ['-timestamp', 'auction_id']

    def __str__(self):
        return f"Auction {self.auction_id} for {self.item.name}"

