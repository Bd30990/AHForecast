from django.contrib import admin, messages
from .models import Auction
from .views import get_valid_access_token
from item_db.models import Item
import requests

@admin.action(description="Fetch Auction House Data")
def fetch_ah_data_action(modeladmin, request, queryset):
    access_token = get_valid_access_token()
    url = "https://us.api.blizzard.com/data/wow/connected-realm/5066/auctions/6?namespace=dynamic-classic1x-us"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for unsuccessful response
        data = response.json()

        for auction_data in data.get("auctions", []):
            # Get or create item in Item model
            item, _ = Item.objects.get_or_create(itemId=auction_data['item']['id'])

            # Check if auction with given ID exists, create new if not
            Auction.objects.get_or_create(
                auction_id=auction_data['id'],
                defaults={
                    'item': item,
                    'bid': auction_data['bid'],
                    'buyout': auction_data['buyout'],
                    'quantity': auction_data['quantity'],
                    'time_left': auction_data['time_left']
                }
            )

        messages.success(request, 'Auction data fetched successfully!')
    except requests.RequestException as e:
        messages.error(request, f"Error fetching auction data: {e}")

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    actions = [fetch_ah_data_action]
