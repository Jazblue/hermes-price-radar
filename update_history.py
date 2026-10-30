import json
from datetime import datetime

try:
    import pytz
    now = datetime.now(pytz.timezone('Europe/London'))
except ImportError:
    from datetime import timezone, timedelta
    now = datetime.now(timezone(timedelta(hours=1)))

ts = now.isoformat()
date_str = now.strftime('%Y%m%d')

with open('data/price-history.json', 'r') as f:
    history = json.load(f)

new_observations = [
    {
        "observation_id": f"obs_{date_str}_90nb10r2_m01820_asus_direct",
        "observed_at": ts,
        "manufacturer_part_number": "90NB10R2-M01820",
        "product_id": "ASUS-Vivobook-M1605-Silver-16GB-512GB",
        "product": "ASUS Vivobook 16 M1605",
        "retailer": "ASUS UK Store",
        "retailer_slug": "asus-uk-store",
        "retailer_product_id": "90NB10R2-M01820",
        "price": 549.99,
        "currency": "GBP",
        "list_price": 599.99,
        "price_type": "standard",
        "availability": "in_stock",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
        "product_url": "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
        "evidence": "Special Price GBP 549.99, Regular Price GBP 599.99. Part Number 90NB10R2-M01820 confirmed.",
        "previous_price": 599.00,
        "change_from_previous": -49.01,
        "change_percentage": -8.2,
        "first_observation_for_product": False
    },
    {
        "observation_id": f"obs_{date_str}_d8wa6ea_abu_johnlewis",
        "observed_at": ts,
        "manufacturer_part_number": "D8WA6EA#ABU",
        "product_id": "HP-15-fd1000nax-Core7-16GB-512GB",
        "product": "HP 15-fd1000nax Laptop",
        "retailer": "John Lewis",
        "retailer_slug": "john-lewis",
        "retailer_product_id": "p115558654",
        "price": 849.99,
        "currency": "GBP",
        "price_type": "standard",
        "availability": "in_stock",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654",
        "product_url": "https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654",
        "evidence": "Price GBP 849.99 confirmed on product page. MPN D8WA6EA#ABU confirmed.",
        "first_observation_for_product": True
    },
    {
        "observation_id": f"obs_{date_str}_d8wa6ea_abu_ao",
        "observed_at": ts,
        "manufacturer_part_number": "D8WA6EA#ABU",
        "product_id": "HP-15-fd1000nax-Core7-16GB-512GB",
        "product": "HP 15-fd1000nax Laptop",
        "retailer": "AO.com",
        "retailer_slug": "ao",
        "retailer_product_id": "d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251",
        "price": 849.99,
        "currency": "GBP",
        "price_type": "standard",
        "availability": "in_stock",
        "verification_status": "PARTIALLY_VERIFIED",
        "verification_method": "search_result",
        "verification_source": "https://ao.com/product/d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251.aspx",
        "product_url": "https://ao.com/product/d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251.aspx",
        "evidence": "Product page found via search. Price not independently confirmed from live page fetch.",
        "counts_toward_lowest_verified": False,
        "first_observation_for_product": True
    },
    {
        "observation_id": f"obs_{date_str}_3xgg3_dell_johnlewis",
        "observed_at": ts,
        "manufacturer_part_number": "3XGG3",
        "product_id": "Dell-16-DC16251-Core5-16GB-512GB",
        "product": "Dell 16 DC16251 Laptop",
        "retailer": "John Lewis",
        "retailer_slug": "john-lewis",
        "retailer_product_id": "p112989884",
        "price": None,
        "currency": "GBP",
        "price_type": "standard",
        "availability": "out_of_stock",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-16gb-ram-512gb-ssd-16-inch/p112989884",
        "product_url": "https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-16gb-ram-512gb-ssd-16-inch/p112989884",
        "evidence": "Product page found but item appears unavailable/out of stock.",
        "first_observation_for_product": True
    }
]

history['observations'].extend(new_observations)
history['_updated_at'] = ts

with open('data/price-history.json', 'w') as f:
    json.dump(history, f, indent=2)

print(f"Updated price-history.json with {len(new_observations)} new observations")
print(f"Total observations: {len(history['observations'])}")
