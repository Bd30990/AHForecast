from django.db import models
from item_db.models import Item

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

