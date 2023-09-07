from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils import timezone
import requests
from decouple import config
from .models import AccessToken, Auction
from item_db.models import Item


def fetch_and_store_access_token():
    url = "https://us.battle.net/oauth/token"
    data = {
        'grant_type': 'client_credentials'
    }
    CLIENT_ID = config('CLIENT_ID')
    CLIENT_SECRET = config('CLIENT_SECRET')
    auth = (CLIENT_ID, CLIENT_SECRET)

    response = requests.post(url, data=data, auth=auth)
    token_data = response.json()

    # Check if 'access_token' is present in the response
    if 'access_token' in token_data:
        # Store in the database
        AccessToken.objects.create(
            access_token=token_data['access_token'],
            token_type=token_data['token_type'],
            expires_in=token_data['expires_in']
        )
        return token_data['access_token']
    else:
        # Optionally log the error or raise a custom exception
        raise ValueError("Failed to fetch access token from the API.")


def get_valid_access_token():
    try:
        # Get the latest token from the database
        token_obj = AccessToken.objects.latest('timestamp')
        if token_obj.is_valid:
            return token_obj.access_token
        else:
            # If it's expired, fetch a new one
            token = fetch_and_store_access_token()
            if not token:
                raise Exception("Failed to fetch a new access token.")
            return token
    except AccessToken.DoesNotExist:
        # If there's no token at all in the database, fetch a new one
        token = fetch_and_store_access_token()
        if not token:
            raise Exception("Failed to fetch a new access token.")
        return token


@staff_member_required
def fetch_ah_data(request):
    access_token = get_valid_access_token()

    url = "https://us.api.blizzard.com/data/wow/connected-realm/5066/auctions/6?namespace=dynamic-classic1x-us"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        for auction_data in data.get("auctions", []):
            # Get or create item in Item model
            item, _ = Item.objects.get_or_create(itemId=auction_data['item']['id'])

            # Check if auction with given ID exists, create new if not
            auction, created = Auction.objects.get_or_create(
                auction_id=auction_data['id'],
                defaults={
                    'item': item,
                    'bid': auction_data['bid'],
                    'buyout': auction_data['buyout'],
                    'quantity': auction_data['quantity'],
                    'time_left': auction_data['time_left']
                }
            )
    except requests.RequestException as e:
        messages.error(request, f"Error fetching auction data: {e}")
        return redirect('admin:index')

    messages.success(request, 'Auction data fetched successfully!')
    return redirect('admin:index')



def index(request):
    return HttpResponse("You're at the ah_api index.")


