import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

# Load products
with open("data/products.json", "r") as f:
    products_data = json.load(f)

products = products_data["products"]

# Products sheet columns
products_header = [
    "Product ID", "Product", "Manufacturer", "Model", "Category",
    "Retailer", "Current Price", "Currency", "Lowest Recorded", "Highest Recorded",
    "Previous Price", "Price Change", "URL", "Availability", "Last Checked"
]

products_rows = []
for pid, p in products.items():
    manufacturer = p.get("manufacturer", "")
    model = p.get("model", "")
    category = p.get("category", "")
    product_name = p.get("product", "")
    lowest_recorded = p.get("lowest_recorded_price", "")
    highest_recorded = p.get("highest_recorded_price", "")
    previous_price = p.get("previous_price", "")
    price_change = p.get("price_change", "")
    last_checked = p.get("last_checked", NOW)
    
    # Iterate retailers
    for rslug, r in p.get("retailers", {}).items():
        retailer = r.get("retailer", "")
        price = r.get("price", "")
        currency = r.get("currency", "GBP")
        availability = r.get("availability", "")
        url = r.get("product_url", "")
        
        row = [
            pid, product_name, manufacturer, model, category,
            retailer, price, currency, lowest_recorded, highest_recorded,
            previous_price, price_change, url, availability, last_checked
        ]
        products_rows.append(row)

# Price History sheet columns
history_header = [
    "Timestamp", "Product ID", "Product", "Retailer", "Price", "Currency", "URL", "Availability"
]

with open("data/price-history.json", "r") as f:
    history_data = json.load(f)

observations = history_data["observations"]
# Take last 100 observations for sheet
recent_obs = observations[-100:] if len(observations) > 100 else observations

history_rows = []
for obs in recent_obs:
    row = [
        obs.get("observed_at", ""),
        obs.get("product_id", ""),
        obs.get("product", ""),
        obs.get("retailer", ""),
        obs.get("price", ""),
        obs.get("currency", "GBP"),
        obs.get("product_url", ""),
        obs.get("availability", "")
    ]
    history_rows.append(row)

# Radar sheet: summary
radar_header = [
    "Product", "Model", "Lowest Verified Price", "Retailer", "Number of Retailers Checked",
    "Last Checked", "Price Change", "Notes"
]

radar_rows = []
for pid, p in products.items():
    lv = p.get("lowest_verified") or {}
    lowest_price = lv.get("price", "")
    retailer_slug = lv.get("retailer_slug", "")
    retailers_checked = lv.get("retailers_checked", 0)
    last_checked = p.get("last_checked", NOW)
    price_change = p.get("price_change", "")
    notes = ""
    
    # Check if price increased significantly
    if price_change and price_change > 0:
        notes = f"Price increased by £{price_change}"
    elif price_change and price_change < 0:
        notes = f"Price dropped by £{abs(price_change)}"
    
    row = [
        p.get("product", ""),
        p.get("model", ""),
        lowest_price, retailer_slug, retailers_checked,
        last_checked, price_change, notes
    ]
    radar_rows.append(row)

# Output as JSON for batch update
output = {
    "products": {"header": products_header, "rows": products_rows},
    "history": {"header": history_header, "rows": history_rows},
    "radar": {"header": radar_header, "rows": radar_rows}
}

with open("data/sheets_payload.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Products rows: {len(products_rows)}")
print(f"History rows: {len(history_rows)}")
print(f"Radar rows: {len(radar_rows)}")