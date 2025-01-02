# NFT Generator

### Automated Generation of Layered NFTs with Metadata

This NFT Generator creates unique NFTs by combining layered image assets (e.g., backgrounds, masks, eyes, bands) and generates corresponding metadata files. It supports conditional logic to ensure traits follow predefined rules, ensuring consistency and uniqueness.

---

## Key Features

- **Layered Image Composition:** Combine multiple layers (e.g., Backgrounds, Masks, Eyes) to generate unique NFTs.
- **Conditional Rules:** Enforce rules to maintain consistency (e.g., specific eye types for specific masks).
- **Automated Metadata Generation:** Creates compliant metadata files for each NFT.
- **Scalable Output:** Supports bulk generation of hundreds of NFTs in one run.
- **Uniqueness Check:** Prevent duplicate NFTs with identical attributes.
- **IPFS Ready:** Metadata and images are structured for easy IPFS upload.

---

## Dependencies

Make sure you have the following installed:

- **Python 3.x**
- **Pillow (PIL)** – Python Imaging Library for image composition
- **JSON** – For metadata generation

Install dependencies:

```bash
pip install pillow
```

## Setup and Configuration
1. Organize Your Layers
Structure your folder as seen in the `layers` folder, or update the code to accommodate your structure.

2. Configuration Rules
Edit the script to define your rules, e.g. this configuration has:

Gray background → Only gray masks.
Purple background → Only purple eyes.

Rules are defined directly in the script under BACKGROUND_RULES and EYE_RULES.

3. Run the Generator
Execute the NFT Generator script:
```bash
python3 main.py
```
Expected Outputs:
/output_nfts: Final PNG images for each NFT.
/metadata: JSON files containing metadata for each NFT.

4. Edit switch_ipfs.py
The IPFS of all the generated metadata is blank, since the images are generated alongside them. Thus, you must upload the images into an IPFS service and retrieve the corresponding link to the online folder to use as the desired IPFS location.
Ensure the desired IPFS is entered in `new_prefix` to ensure that metadata points to the correct image location.

Run the script.

```bash
python3 switch_ipfs.py
```

This will swap the "blank" to the desired IPFS link for all the generated metadata.

## How it Works
The generator selects random traits from each layer (background, mask, eyes, band).
Applies predefined rules to ensure trait compatibility.
Combines image layers using Pillow (PIL).
Generates a JSON metadata file per NFT.
Ensures no duplicate NFTs are generated.

This configuration prints 3 separate NFTs and 3 metadata files, this is because it was built for a dynamic NFT which required different images and metadata corresponding to such. Thus, you can delete the code responsible for metadata and NFT generation for the `_tears` and `_blush` postfix of each.

## Customization
Add New Layers: Add additional image files to `/layers` (e.g., new masks, bands).
Update Rules: Modify `BACKGROUND_RULES` and `EYE_RULES` in the script.
Adjust Resolution: Update the output image resolution in the script (default is 3000x3000).
Update Metadata Template: Customize the structure of metadata in the script.

## Contact
Twitter: @0xpoot_poot
Email: 0xpoot@gmail.com
