import json

# Read from the current file
with open('raw-data.json', 'r') as f:
    data = json.load(f)

# Dump the JSON data in a pretty format
pretty_data = json.dumps(data, indent=4)

# Write the prettified data to a new file
with open('item-data.json', 'w') as f:
    f.write(pretty_data)
