import json

# Read existing data.json
with open('data/products.json', 'r') as f:
    d = json.load(f)

# Add 3 new products
new_products = {
    '6CH4H': {
        'product_id': 'dell-inspiron-15-3530-6ch4h',
        'brand': 'Dell',
        'model': 'Inspiron 15 3530',
        'manufacturer_part_number': '6CH4H',
        'model_number': '3530',
        'alternate_part_numbers': [],
        'marketing_title': 'Dell Inspiron 15 3530',
        'key_specs': {
            'cpu': 'Intel Core i5-1334U',
            'ram': '16GB DDR4',
            'storage': '512GB NVMe M.2 SSD',
            'display': '15.6in WUXGA IPS 1920x1200',
            'gpu': 'Intel Iris Xe Graphics',
            'os': 'Windows 11 Home 64-bit',
            'colour': 'Carbon Black'
        },
        'spec_conflicts': [],
        'retailers': {
            'esupply': {
                'retailer': 'eSupply',
                'retailer_slug': 'esupply',
                'retailer_product_id': '6CH4H',
                'listing_title': 'DELL Inspiron 3530 Intel Core i5 1334U 16GB RAM 512GB SSD 16" Windows 11 Home Copilot+ Laptop',
                'product_url': 'https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/',
                'price': 524.16,
                'currency': 'GBP',
                'list_price': None,
                'price_type': 'standard',
                'availability': 'in_stock',
                'last_verified': '2026-10-03T00:45:00Z',
                'verification_status': 'VERIFIED',
                'verification_method': 'direct_page_fetch',
                'verification_source': 'https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/',
                'evidence': 'Body read at source. SKU 6CH4H confirmed. Full spec table matches. Add to Cart present.',
                'block_reason': None,
                'checked_at': '2026-10-03T00:45:00Z'
            }
        },
        'lowest_verified': {
            'price': 524.16,
            'currency': 'GBP',
            'retailer_slug': 'esupply',
            'product_url': 'https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/',
            'retailers_checked': 1,
            'retailers_verified': 1,
            'retailers_verified_and_purchasable': 1,
            'computed_at': '2026-10-03T00:45:00Z'
        },
        'tracking': {
            'enabled': True,
            'added_at': '2026-10-03T00:45:00Z',
            'notes': 'Verified at eSupply with price £524.16. Windows 11 Pro. Mainstream pricing.'
        }
    },
    '3XGG3': {
        'product_id': 'dell-16-dc16251-3xgg3',
        'brand': 'Dell',
        'model': 'Dell 16 DC16251',
        'manufacturer_part_number': '3XGG3',
        'model_number': 'DC16251',
        'alternate_part_numbers': [],
        'marketing_title': 'Dell 16 DC16251',
        'key_specs': {
            'cpu': 'Intel Core 5 120U',
            'ram': '16GB LPDDR5X',
            'storage': '512GB NVMe M.2 SSD',
            'display': '16in 2K 1920x1200 16:10 IPS',
            'gpu': 'Intel Graphics',
            'os': 'Windows 11 Home 64-bit',
            'colour': 'Silver'
        },
        'spec_conflicts': [
            {
                'field': 'ram',
                'resolved': False,
                'note': 'LPDDR5X is soldered/onboard, not user-upgradable SO-DIMM. Different from DDR4/DDR5 SO-DIMM in other tracked products.',
                'values': [
                    {
                        'value': '16GB LPDDR5X-7500 onboard',
                        'source': 'johnlewis.com',
                        'source_trust': 'retailer_page'
                    }
                ]
            }
        ],
        'retailers': {
            'johnlewis': {
                'retailer': 'John Lewis',
                'retailer_slug': 'johnlewis',
                'retailer_product_id': '82715313',
                'listing_title': 'Dell 16 DC16251 Laptop, Intel Core 5 Processor, 16GB RAM, 512GB SSD, 16" Full HD+, Silver',
                'product_url': 'https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-processor-16gb-ram-512gb-ssd-16-full-hd-silver/p115762767',
                'price': 749.00,
                'currency': 'GBP',
                'list_price': None,
                'price_type': 'standard',
                'availability': 'in_stock',
                'last_verified': '2026-10-03T00:45:00Z',
                'verification_status': 'VERIFIED',
                'verification_method': 'direct_page_fetch',
                'verification_source': 'https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-processor-16gb-ram-512gb-ssd-16-full-hd-silver/p115762767',
                'evidence': 'Body read at source. Manufacturer part number (MPN) 3XGG3 in spec block. Price £749.00. Add to basket present. 2-year guarantee. Specs: Intel Core 5 120U, 16GB LPDDR5X, 512GB PCIe Gen4 NVMe, 16" 2K 16:10 IPS, Intel Graphics, Windows 11 Home.',
                'block_reason': None,
                'checked_at': '2026-10-03T00:45:00Z'
            }
        },
        'lowest_verified': {
            'price': 749.00,
            'currency': 'GBP',
            'retailer_slug': 'johnlewis',
            'product_url': 'https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-processor-16gb-ram-512gb-ssd-16-full-hd-silver/p115762767',
            'retailers_checked': 1,
            'retailers_verified': 1,
            'retailers_verified_and_purchasable': 1,
            'computed_at': '2026-10-03T00:45:00Z'
        },
        'tracking': {
            'enabled': True,
            'added_at': '2026-10-03T00:45:00Z',
            'notes': '16" screen with LPDDR5X soldered RAM (not upgradable). Core 5 120U. Windows 11 Home. £749 at John Lewis (upper bound of range). LPDDR5X is soldered/onboard.'
        }
    },
    'D8WA6EA#ABU': {
        'product_id': 'hp-15-fd1000nax-d8wa6ea-abu',
        'brand': 'HP',
        'model': 'HP 15-fd1000nax',
        'manufacturer_part_number': 'D8WA6EA#ABU',
        'model_number': '15-fd1000nax',
        'alternate_part_numbers': [],
        'marketing_title': 'HP 15-fd1000nax',
        'key_specs': {
            'cpu': 'Intel Core 7 (13th Gen)',
            'ram': '16GB DDR4-3200',
            'storage': '512GB NVMe M.2 SSD',
            'display': '15.6in FHD IPS 1920x1200',
            'gpu': 'Intel Graphics',
            'os': 'Windows 11 Home 64-bit',
            'colour': 'Jet Black'
        },
        'spec_conflicts': [],
        'retailers': {
            'johnlewis': {
                'retailer': 'John Lewis',
                'retailer_slug': 'johnlewis',
                'retailer_product_id': '82711767',
                'listing_title': 'HP 15-fd1000nax Laptop, Intel Core 7 Processor, 16GB RAM, 512GB SSD, 15.6" Full HD, Jet Black',
                'product_url': 'https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654',
                'price': 699.99,
                'currency': 'GBP',
                'list_price': 899.99,
                'price_type': 'standard',
                'availability': 'in_stock',
                'last_verified': '2026-10-03T00:45:00Z',
                'verification_method': 'direct_page_fetch',
                'verification_source': 'https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654',
                'evidence': 'Body read at source. Manufacturer part number (MPN) D8WA6EA #ABU in spec block. Price £699.99 (was £899.99). Add to basket present. 2-year guarantee. Specs: Intel Core 7 (10c/12t, up to 5.0GHz), 16GB DDR4-3200 (2x8GB), 512GB PCIe NVMe, 15.6" FHD 1920x1080, Intel Graphics, Windows 11 Home.',
                'block_reason': None,
                'checked_at': '2026-10-03T00:45:00Z'
            }
        },
        'lowest_verified': {
            'price': 699.99,
            'currency': 'GBP',
            'retailer_slug': 'johnlewis',
            'product_url': 'https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654',
            'retailers_checked': 1,
            'retailers_verified': 1,
            'retailers_verified_and_purchasable': 1,
            'computed_at': '2026-10-03T00:45:00Z'
        },
        'tracking': {
            'enabled': True,
            'added_at': '2026-10-03T00:45:00Z',
            'notes': 'Intel Core 7 (i7-tier, 10c/12t, up to 5.0GHz) - higher tier than target Core 5/i5. £699.99 at John Lewis (was £899.99, promo price). Power adapter sold separately (USB-C 65W). Windows 11 Home. Verified at John Lewis.'
        }
    }
}

# Read existing data
with open('C:/Users/Administrator/hermes-price-radar/data/products.json', 'r') as f:
    d = json.load(f)

# Update products dict
d['products'].update(new_products)

# Write back
with open('C:/Users/Administrator/hermes-price-radar/data/products.json', 'w') as f:
    json.dump(d, f, indent=2)

print('Success: 3 products added. Total products:', len(d['products']))