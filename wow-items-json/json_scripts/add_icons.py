import json

# Load the JSON data
with open('item-data.json', 'r') as json_file:
    data = json.load(json_file)

# Update each item to include the icon_image path
for item in data:
    icon_name = item.get('icon', '')
    if icon_name:
        item['icon_image'] = f"icon_images/{icon_name}.png"

# Save the updated JSON data back to the file
with open('item-data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Updated icon_image paths in the JSON data.")
