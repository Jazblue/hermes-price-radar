import json

# Read the price-history.json file
with open('C:/Users/Administrator/hermes-price-radar/data/price-history.json', 'r') as f:
    content = f.read()

# Parse to get the data structure
data = json.loads(content)

# New observations to add
new_observations = [
    {
        "observation_id": "obs_20261003t0045_6ch4h_esupply",
        "observed_at": "2026-10-03T00:45:00Z",
        "manufacturer_part_number": "6CH4H",
        "product_id": "dell-inspiron-15-3530-6ch4h",
        "product": "Dell Inspiron 15 3530",
        "retailer": "eSupply",
        "retailer_slug": "esupply",
        "retailer_product_id": "6CH4H",
        "price": 524.16,
        "currency": "GBP",
        "list_price": None,
        "price_type": "standard",
        "availability": "in_stock",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/",
        "product_url": "https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/",
        "evidence": "Body read at source. 'Dell SKU: 6CH4H' printed on page. Full spec table confirms Intel Core i5-1334U, 16GB DDR4, 512GB NVMe M.2 SSD, 15.6\" FHD 120Hz IPS, Intel Iris Xe Graphics, Windows 11 Pro. Cart control present.",
        "counts_toward_lowest_verified": True,
        "first_observation_for_product": True,
        "change_note": "NEW RETAILER DISCOVERED. First observation for this product. Establishes baseline."
    },
    {
        "observation_id": "obs_20261003t0045_3xgg3_johnlewis",
        "observed_at": "2026-10-03T00:45:00Z",
        "manufacturer_part_number": "3XGG3",
        "product_id": "dell-16-dc16251-3xgg3",
        "product": "Dell 16 DC16251",
        "retailer": "John Lewis",
        "retailer_slug": "johnlewis",
        "retailer_product_id": "82715313",
        "price": 749.00,
        "currency": "GBP",
        "list_price": None,
        "price_type": "standard",
        "availability": "in_stock",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-processor-16gb-ram-512gb-ssd-16-full-hd-silver/p115762767",
        "product_url": "https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-processor-16gb-ram-512gb-ssd-16-full-hd-silver/p115762767",
        "evidence": "Body read at source. 'Manufacturer part number (MPN) 3XGG3' in spec block. Price £749.00. Add to basket present. 2-year guarantee. Specs: Intel Core 5 120U, 16GB LPDDR5X, 512GB PCIe Gen4 NVMe, 16\" 2K 1920x1200, Intel Graphics, Windows 11 Home.",
        "counts_toward_lowest_verified": True,
        "first_observation_for_product": True,
        "change_note": "NEW RETAILER DISCOVERED. First observation for this product. Establishes baseline. 16\" screen with LPDDR5X soldered RAM (not upgradable). Core 5 120U. Windows 11 Home. £749 at John Lewis (upper bound of range). LPDDR5X is soldered/onboard - spec_conflict recorded on product."
    },
    {
        "observation_id": "obs_20261003t0045_d8wa6ea_abu_johnlewis",
        "observed_at": "2026-10-03T00:45:00Z",
        "manufacturer_part_number": "D8WA6EA#ABU",
        "product_id": "hp-15-fd1000nax-d8wa6ea-abu",
        "product": "HP 15-fd1000nax",
        "retailer": "John Lewis",
        "retailer_slug": "johnlewis",
        "retailer_product_id": "82711767",
        "price": 699.99,
        "currency": "GBP",
        "list_price": 899.99,
        "price_type": "standard",
        "availability": "in_stock",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654",
        "product_url": "https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654",
        "evidence": "Body read at source. 'Manufacturer part number (MPN) D8WA6EA #ABU' in spec block. Price £699.99 (was £899.99). Add to basket present. 2-year guarantee. Specs: Intel Core 7 (10c/12t, up to 5.0GHz), 16GB DDR4-3200 (2x8GB), 512GB PCIe NVMe, 15.6\" FHD 1920x1080, Intel Graphics, Windows 11 Home. Power adapter sold separately (USB-C 65W).",
        "counts_toward_lowest_verified": True,
        "first_observation_for_product": True,
        "change_note": "NEW RETAILER DISCOVERED. First observation for this product. Establishes baseline. Intel Core 7 (i7-tier, 10c/12t, up to 5.0GHz) - higher tier than target Core 5/i5. £699.99 at John Lewis (was £899.99, promo price). Power adapter sold separately (USB-C 65W). Windows 11 Home. Verified at John Lewis."
    }
]

# Read the file content
with open('C:/Users/Administrator/hermes-price-radar/data/price-history.json', 'r') as f:
    content = f.read()

# Parse JSON
data = json.loads(content)

# Add the new observations
data['observations'].extend(new_observations)

# Write back
with open('C:/Users/Administrator/hermes-price-radar/data/price-history.json', 'w') as f:
    json.dump(data, f, indent=2)

print('Successfully added 3 new observations to price-history.json')
print('Total observations:', len(data['observations']))