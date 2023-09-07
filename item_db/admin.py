from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from .models import Item
from ah_api.models import Auction
from django.template.loader import render_to_string
import json

class ItemAdmin(admin.ModelAdmin):
    change_form_template = 'item_db/change_form.html'
    search_fields = ['name']
    
    def get_changeform_initial_data(self, request):
        item_id = request.GET.get('item_id')
        initial = super().get_changeform_initial_data(request)
        initial['other_item_fields'] = item_id
        return initial

    def change_view(self, request, object_id, form_url='', extra_context=None):
        item = self.get_object(request, object_id)
        auctions = Auction.objects.filter(item=item)

        # Create a message with auction information
        if auctions.exists():
            message = 'Auctions:<br>'
            for auction in auctions:
                buyout_gold = auction.buyout // 10000
                buyout_silver = (auction.buyout % 10000) // 100
                buyout_copper = auction.buyout % 100
                timestamp_formatted = auction.timestamp.strftime('%m/%d/%Y %I:%M%p')
                message += f'Auction ID: {auction.auction_id}, Quantity: {auction.quantity}, Buyout Amount: {buyout_gold}g {buyout_silver}s {buyout_copper}c, Timestamp: {timestamp_formatted}<br>'
        else:
            message = 'No auctions found for this item.'
        
        messages.info(request, format_html(message))
        
        # Get auction data for the chart
        auctions = Auction.objects.filter(item=item).order_by('timestamp')
        timestamps = [auction.timestamp.strftime('%m/%d/%Y %I:%M %p') for auction in auctions]
        buyout_prices = [auction.buyout for auction in auctions]
        quantity = [auction.quantity for auction in auctions]
    
        context = {
            'timestamps': json.dumps(timestamps),
            'buyout_prices': json.dumps(buyout_prices),
            'quantity': json.dumps(quantity)
        }

        chart_html = render_to_string('item_db/item_chart.html', context)
        extra_context = extra_context or {}
        extra_context['chart_html'] = chart_html

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(Item, ItemAdmin)
