from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Item
from ah_api.models import Auction
from .serializers import ItemSerializer
import pandas as pd


def index(request):
    return HttpResponse("You're at the item_db index.")

# def search(request):
#     query = request.GET.get('q')
#     items = []
#     if query:
#         items = Item.objects.filter(name__icontains=query)
#     return render(request, )


# Query ex: http://localhost:8000/item_db/api/search/?q=Linen Cloth
@api_view(['GET'])
def search_api(request):
    query = request.GET.get('q', '')
    items = Item.objects.filter(name__icontains=query)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


def item_auction_data(request, item_id):
    item = Item.objects.get(id=item_id)
    auctions = Auction.objects.filter(item=item).order_by('timestamp')

    timestamps = [auction.timestamp.strftime('%m/%d/%Y %I:%M %p') for auction in auctions]

    # Convert buyout prices to string format and decimal format
    buyout_prices_gsc = []
    buyout_prices_decimal = []
    for auction in auctions:
        gold = auction.buyout // 10000
        silver = (auction.buyout % 10000) // 100
        copper = auction.buyout % 100
        buyout_prices_gsc.append(f"{gold}g {silver}s {copper}c")
        buyout_prices_decimal.append(gold + silver/100 + copper/10000)

    data = {
        'timestamps': timestamps,
        'buyout_prices': buyout_prices_gsc,
        'buyout_prices_decimal': buyout_prices_decimal,
        'item_name': item.name,
    }

    return JsonResponse(data)



