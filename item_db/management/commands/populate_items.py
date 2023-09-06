# Import necessary modules
from django.core.management.base import BaseCommand
import json
from item_db.models import Item
from item_db.models import item_icon_image_path  # Import your custom path function

class Command(BaseCommand):
    help = 'Populates the items database from a JSON file'

    def handle(self, *args, **options):
        # Path to the JSON file
        json_file_path = 'wow-items-json/item-data.json'
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)

            for item_data in data:
                # Check if an item with the same itemId already exists
                existing_item = Item.objects.filter(itemId=item_data['itemId']).first()
                if existing_item:
                    # Item with the same itemId already exists, update its fields
                    existing_item.name = item_data['name']
                    existing_item.icon = item_data['icon']
                    existing_item.item_class = item_data.get('class', '')
                    existing_item.subclass = item_data.get('subclass', '')
                    existing_item.sellPrice = item_data.get('sellPrice', 0)
                    existing_item.quality = item_data.get('quality', '')
                    existing_item.itemLevel = item_data.get('itemLevel', 0)
                    existing_item.requiredLevel = item_data.get('requiredLevel', 0)
                    existing_item.slot = item_data.get('slot', '')
                    # Update the icon_image path
                    existing_item.icon_image = item_icon_image_path(existing_item, item_data['icon_image'])
                    existing_item.save()
                else:
                    # Item doesn't exist, create a new one
                    # Use the item_icon_image_path function to set the icon_image path
                    Item.objects.create(
                        itemId=item_data['itemId'],
                        name=item_data['name'],
                        icon=item_data['icon'],
                        item_class=item_data.get('class', ''),
                        subclass=item_data.get('subclass', ''),
                        sellPrice=item_data.get('sellPrice', 0),
                        quality=item_data.get('quality', ''),
                        itemLevel=item_data.get('itemLevel', 0),
                        requiredLevel=item_data.get('requiredLevel', 0),
                        slot=item_data.get('slot', ''),
                        icon_image=item_icon_image_path(None, item_data['icon_image'])
                    )

            self.stdout.write(self.style.SUCCESS('Successfully populated items database from JSON'))
