import json, datetime

now = datetime.datetime.now(datetime.timezone.utc).isoformat()

with open('data/products.json') as f:
    data = json.load(f)

# Update 90NB15F1-M00A60 - AO now has £470
data['products']['90NB15F1-M00A60']['retailers']['ao'] = {
    'retailer': 'AO',
    'retailer_slug': 'ao',
    'retailer_product_id': 'M1607KA-MB148W',
    'listing_title': 'ASUS Vivobook 16 M1607KA-MB148W 16 Copilot+ Laptop - Blue',
    'product_url': 'https://ao.com/product/m1607kamb148w-asus-vivobook-16-m1607kamb148w-laptop--blue-107583-251.aspx',
    'price': 470.00,
    'currency': 'GBP',
    'list_price': 749.00,
    'price_type': 'standard',
    'availability': 'in_stock',
    'last_verified': now,
    'verification_status': 'VERIFIED',
    'verification_method': 'direct_page_fetch',
    'verification_source': 'https://ao.com/product/m1607kamb148w-asus-vivobook-16-m1607kamb148w-laptop--blue-107583-251.aspx',
    'evidence': 'AO product page shows £470 (was £749), Save £279. Model M1607KA-MB148W confirmed. Add to basket present. In stock with delivery from Tue 27th Oct.',
    'block_reason': None,
    'checked_at': now
}
data['products']['90NB15F1-M00A60']['lowest_verified'] = {
    'price': 470.00,
    'currency': 'GBP',
    'retailer_slug': 'ao',
    'product_url': 'https://ao.com/product/m1607kamb148w-asus-vivobook-16-m1607kamb148w-laptop--blue-107583-251.aspx',
    'retailers_checked': 6,
    'retailers_verified': 4,
    'retailers_verified_and_purchasable': 3,
    'computed_at': now
}
if 'price_changes' not in data['products']['90NB15F1-M00A60']:
    data['products']['90NB15F1-M00A60']['price_changes'] = []
data['products']['90NB15F1-M00A60']['price_changes'].append({
    'from_price': 499.00,
    'to_price': 470.00,
    'change': -29.00,
    'change_percent': -5.8,
    'detected_at': now,
    'reason': 'AO now offering £470 (was £749), new lowest verified price'
})

# Update 90NB10R2-M01820 - ASUS UK dropped to £499.99
data['products']['90NB10R2-M01820']['retailers']['asus-uk-store']['price'] = 499.99
data['products']['90NB10R2-M01820']['retailers']['asus-uk-store']['list_price'] = 549.99
data['products']['90NB10R2-M01820']['retailers']['asus-uk-store']['last_verified'] = now
data['products']['90NB10R2-M01820']['retailers']['asus-uk-store']['evidence'] = 'ASUS UK store page shows Special Price GBP 499.99 / Regular Price GBP 549.99 / Save GBP 50. Model M1605YA-MB601W, Part Number 90NB10R2-M01820 confirmed.'
data['products']['90NB10R2-M01820']['lowest_verified'] = {
    'price': 499.00,
    'currency': 'GBP',
    'retailer_slug': 'argos',
    'product_url': 'https://www.argos.co.uk/product/7956449',
    'retailers_checked': 5,
    'retailers_verified': 3,
    'retailers_verified_and_purchasable': 2,
    'computed_at': now
}
if 'price_changes' not in data['products']['90NB10R2-M01820']:
    data['products']['90NB10R2-M01820']['price_changes'] = []
data['products']['90NB10R2-M01820']['price_changes'].append({
    'from_price': 549.99,
    'to_price': 499.99,
    'change': -50.00,
    'change_percent': -9.1,
    'detected_at': now,
    'reason': 'ASUS UK Store dropped price from £549.99 to £499.99 (Save £50)'
})

# Update 3XGG3 - Dell UK now £729
data['products']['3XGG3']['retailers']['dell-uk'] = {
    'retailer': 'Dell UK',
    'retailer_slug': 'dell-uk',
    'retailer_product_id': 'cndc1625104',
    'listing_title': 'Dell 16 Laptop DC16251 Intel Core 5 120U 16GB 512GB SSD',
    'product_url': 'https://www.dell.com/en-uk/shop/laptops-2-in-1-pcs/dell-16-laptop/spd/dell-dc16251-laptop/cndc1625104?view=configurations',
    'price': 729.00,
    'currency': 'GBP',
    'list_price': None,
    'price_type': 'standard',
    'availability': 'in_stock',
    'last_verified': now,
    'verification_status': 'VERIFIED',
    'verification_method': 'direct_page_fetch',
    'verification_source': 'https://www.dell.com/en-uk/shop/laptops-2-in-1-pcs/dell-16-laptop/spd/dell-dc16251-laptop/cndc1625104?view=configurations',
    'evidence': 'Dell UK product page shows £729.00 for Dell 16 Laptop DC16251 with Intel Core 5 120U, 16GB DDR5, 512GB SSD, 16" 2K display. Order code cndc1625104. Buy Now/Add to Basket present.',
    'block_reason': None,
    'checked_at': now
}
data['products']['3XGG3']['lowest_verified'] = {
    'price': 729.00,
    'currency': 'GBP',
    'retailer_slug': 'dell-uk',
    'product_url': 'https://www.dell.com/en-uk/shop/laptops-2-in-1-pcs/dell-16-laptop/spd/dell-dc16251-laptop/cndc1625104?view=configurations',
    'retailers_checked': 3,
    'retailers_verified': 2,
    'retailers_verified_and_purchasable': 2,
    'computed_at': now
}
if 'price_changes' not in data['products']['3XGG3']:
    data['products']['3XGG3']['price_changes'] = []
data['products']['3XGG3']['price_changes'].append({
    'from_price': 999.00,
    'to_price': 729.00,
    'change': -270.00,
    'change_percent': -27.0,
    'detected_at': now,
    'reason': 'Dell UK dropped price from £999 to £729 (new config launched)'
})

# Update D8WA6EA#ABU - John Lewis increased to £849.99
data['products']['D8WA6EA#ABU']['retailers']['johnlewis']['price'] = 849.99
data['products']['D8WA6EA#ABU']['retailers']['johnlewis']['last_verified'] = now
data['products']['D8WA6EA#ABU']['retailers']['johnlewis']['evidence'] = 'John Lewis product page shows £849.99 (was £699.99). MPN D8WA6EA#ABU confirmed. In stock with free delivery.'
data['products']['D8WA6EA#ABU']['lowest_verified'] = {
    'price': 849.99,
    'currency': 'GBP',
    'retailer_slug': 'johnlewis',
    'product_url': 'https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654',
    'retailers_checked': 4,
    'retailers_verified': 2,
    'retailers_verified_and_purchasable': 1,
    'computed_at': now
}
if 'price_changes' not in data['products']['D8WA6EA#ABU']:
    data['products']['D8WA6EA#ABU']['price_changes'] = []
data['products']['D8WA6EA#ABU']['price_changes'].append({
    'from_price': 699.99,
    'to_price': 849.99,
    'change': 150.00,
    'change_percent': 21.4,
    'detected_at': now,
    'reason': 'John Lewis increased price from £699.99 to £849.99'
})

data['_updated_at'] = now

with open('data/products.json', 'w') as f:
    json.dump(data, f, indent=2)

print('products.json updated successfully')
print('Changes:')
print('  90NB15F1-M00A60: £499 -> £470 (AO new lowest, -£29)')
print('  90NB10R2-M01820: £549.99 -> £499.99 (ASUS UK drop, -£50)')
print('  3XGG3: £999 -> £729 (Dell UK new config, -£270)')
print('  D8WA6EA#ABU: £699.99 -> £849.99 (John Lewis increase, +£150)')
