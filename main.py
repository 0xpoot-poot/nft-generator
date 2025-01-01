from PIL import Image
import random
import os
import json


# define layer paths
LAYER_PATHS = {
    "backgrounds": "layers/backgrounds",
    "masks": "layers/masks",
    "eyes": "layers/eyes",
    "bands": "layers/bands",
    "tears": "layers/tears",
    "blush": "layers/blush"
}

# output folders
OUTPUT_IMAGE_PATH = "output_nfts"
OUTPUT_METADATA_PATH = "output_metadata"
ATTRIBUTE_LOG_PATH = os.path.join(OUTPUT_METADATA_PATH, "attributes.json")

os.makedirs(OUTPUT_IMAGE_PATH, exist_ok=True)
os.makedirs(OUTPUT_METADATA_PATH, exist_ok=True)

# rules
BACKGROUND_RULES = {
    "gray": "mask_gray",
    "purp": "mask_purple",
    "red": "mask_red",
    "white": "mask_white"
}

EYE_RULES = {
    "mask_gray": ["mask_white", "mask"],
    "mask_white": ["mask_white", "mask"],
    "mask_purple": ["mask_purp", "mask"],
    "mask_red": ["mask_red", "mask"],
    "mask4": [None]
}

# Load existing attributes
if os.path.exists(ATTRIBUTE_LOG_PATH):
    with open(ATTRIBUTE_LOG_PATH, 'r') as f:
        existing_attributes = json.load(f)
else:
    existing_attributes = []

# get random file from a folder
def get_random_file(folder):
    chosen = random.choice(os.listdir(folder))
    if chosen == ".DS_Store":
        return get_random_file(folder)
    else:
        return chosen

# generate NFT
def generate_nft(nft_id):
    metadata = {}
    
    # select background
    bg_color = random.choice(list(BACKGROUND_RULES.keys()))
    background_files = [f for f in os.listdir(LAYER_PATHS['backgrounds']) if bg_color in f]
    background_file = random.choice(background_files)
    metadata["Background"] = background_file
    background = Image.open(os.path.join(LAYER_PATHS['backgrounds'], background_file)).convert("RGBA")
    
    # select compatible mask
    mask_folder = os.path.join(LAYER_PATHS['masks'])
    mask_files = [f for f in os.listdir(LAYER_PATHS['masks']) if bg_color in f]
    mask_file = random.choice(mask_files)
    metadata["Mask"] = mask_file
    mask = Image.open(os.path.join(mask_folder, mask_file)).convert("RGBA")
    
    # select compatible eyes (if not mask4)
    eye = None
    if "mask4" not in mask_file:
        eye_folder_main = os.path.join(LAYER_PATHS['eyes'])
        eye_folders = [f for f in os.listdir(eye_folder_main) if bg_color in f]
        eye_folders.append("mask")
        if eye_folders:
            eye_folder = os.path.join(eye_folder_main, random.choice(eye_folders))
            eye_files = [f for f in os.listdir(eye_folder) if bg_color in f or "mask_" in f]
            eye_file = random.choice(eye_files)
            metadata["Eyes"] = eye_file
            eye = Image.open(os.path.join(eye_folder, eye_file)).convert("RGBA")
    else:
        metadata["Eyes"] = "None"

    # select random band
    band_folder = get_random_file(os.path.join(LAYER_PATHS['bands']))
    band_file = get_random_file(os.path.join(LAYER_PATHS['bands'], band_folder))
    metadata["Band"] = f"{band_folder}/{band_file}"
    band = Image.open(os.path.join(LAYER_PATHS['bands'], band_folder, band_file)).convert("RGBA")

    # select random tear
    tear_file = get_random_file(os.path.join(LAYER_PATHS['tears']))
    metadata["Tear"] = tear_file
    tear = Image.open(os.path.join(LAYER_PATHS['tears'], tear_file)).convert("RGBA")
    
    # select random blush
    blush_file = get_random_file(os.path.join(LAYER_PATHS['blush']))
    metadata["Blush"] = blush_file
    blush = Image.open(os.path.join(LAYER_PATHS['blush'], blush_file)).convert("RGBA")

    # Check for duplicate
    attribute_set = (metadata["Background"], metadata["Mask"], metadata["Eyes"], metadata["Band"])
    if attribute_set in existing_attributes:
        print(f"⚠️ Duplicate detected for NFT {nft_id}, regenerating...")
        generate_nft(nft_id) # regenerate nft
        return
    
    # combine layers
    final_image = background
    final_image = Image.alpha_composite(final_image, mask)
    if eye:
        final_image = Image.alpha_composite(final_image, eye)
    final_image = Image.alpha_composite(final_image, band)

    final_image_tears = background
    final_image_tears = Image.alpha_composite(final_image_tears, mask)
    if eye:
        final_image_tears = Image.alpha_composite(final_image_tears, eye)
    final_image_tears = Image.alpha_composite(final_image_tears, band)
    final_image_tears = Image.alpha_composite(final_image_tears, tear)

    final_image_blush = background
    final_image_blush = Image.alpha_composite(final_image_blush, mask)
    if eye:
        final_image_blush = Image.alpha_composite(final_image_blush, eye)
    final_image_blush = Image.alpha_composite(final_image_blush, band)
    final_image_blush = Image.alpha_composite(final_image_blush, blush)

    # save final images
    output_image_folder = os.path.join(OUTPUT_IMAGE_PATH, f"nft_{nft_id}")
    os.makedirs(output_image_folder, exist_ok=True)
    output_image_file = os.path.join(output_image_folder, f"nft_{nft_id}.png")
    final_image = final_image.resize((3000, 3000))
    final_image.save(output_image_file)
    output_image_file = os.path.join(output_image_folder, f"nft_{nft_id}_tears.png")
    final_image_tears = final_image_tears.resize((3000, 3000))
    final_image_tears.save(output_image_file)
    output_image_file = os.path.join(output_image_folder, f"nft_{nft_id}_blush.png")
    final_image_blush = final_image_blush.resize((3000, 3000))
    final_image_blush.save(output_image_file)
    print(f"✅ NFT {nft_id} saved to {output_image_file}")
        
    # Save unique attributes
    existing_attributes.append(attribute_set)
    with open(ATTRIBUTE_LOG_PATH, 'w') as f:
        json.dump(existing_attributes, f, indent=4)
    
    # generate metadata
    metadata_file = os.path.join(OUTPUT_METADATA_PATH, f"nft_{nft_id}.json")
    metadata_content = {
        "name": f"Masked #{nft_id}",
        "description": "A mysterious mask NFT reflecting wallet activity.",
        "image": f"ipfs://.../nft_{nft_id}.png",
        "attributes": [
            {"trait_type": "Background", "value": metadata["Background"]},
            {"trait_type": "Mask", "value": metadata["Mask"]},
            {"trait_type": "Eyes", "value": metadata["Eyes"]},
            {"trait_type": "Band", "value": metadata["Band"]},
            {"trait_type": "Tear", "value": metadata["Tear"]},
            {"trait_type": "Blush", "value": metadata["Blush"]}
        ]
    }
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata_content, f, indent=4)
    print(f"✅ Metadata for NFT {nft_id} saved to {metadata_file}")
    print()

# generate multiple NFTs
def generate_nft_collection(count):
    for i in range(1, count + 1):
        generate_nft(i)

# generate 200 NFTs
generate_nft_collection(200)