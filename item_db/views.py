from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Item
from .serializers import ItemSerializer


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
