import os
import json
import re


# Directory containing JSON files
json_dir = "output_metadata"

print(os.path.exists(json_dir))
if not os.path.exists(json_dir):
    os.makedirs(json_dir)

# Old and new IPFS prefixes
old_prefix = "blank" # defined as 'blank' in the metadata upon generation
new_prefix = "https://tan-labour-roundworm-161.mypinata.cloud/ipfs/bafybeiavz2i3hx43spsjwltgmdzyrnsyvlbdjjzgd4y37ihsmhsjd3wzg4"

# Iterate through all JSON files in the directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json') and filename.startswith('nft_'):
        file_path = os.path.join(json_dir, filename)
        
        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Update the image URL
        if 'image' in data:
            data['image'] = data['image'].replace(old_prefix, new_prefix)
        
        # Write the updated data back to the file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

print("Updated image URLs in all JSON files")
