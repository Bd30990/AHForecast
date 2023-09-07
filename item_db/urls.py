from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/search/", views.search_api, name="search_api"),
    path('item_auction_data/<int:item_id>/', views.item_auction_data, name='item_auction_data'),
]
