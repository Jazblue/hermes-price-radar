import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
TODAY = "2026-10-29"

# Load existing data
with open("data/products.json", "r") as f:
    products_data = json.load(f)

with open("data/price-history.json", "r") as f:
    history_data = json.load(f)

products = products_data["products"]
observations = history_data["observations"]

obs_counter = 100  # avoid ID collisions

# ── Product 1: 90NB15F1-M00A60 (ASUS Vivobook AI 16) ─────────────────────
# AO: £470 unchanged. New: Argos £629.99 verified in stock.
p1 = products["90NB15F1-M00A60"]
p1["retailers"]["argos"] = {
    "retailer": "Argos",
    "retailer_slug": "argos",
    "retailer_product_id": "7741159",
    "listing_title": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
    "product_url": "https://www.argos.co.uk/product/7741159",
    "price": 629.99,
    "currency": "GBP",
    "list_price": None,
    "price_type": "standard",
    "availability": "in_stock",
    "last_verified": NOW,
    "verification_status": "VERIFIED",
    "verification_method": "web_search_discovery",
    "verification_source": "https://www.google.com/search?q=ASUS+Vivobook+AI+16+90NB15F1-M00A60+site:argos.co.uk",
    "evidence": "Argos search result confirmed product 7741159 as ASUS Vivobook AI 16in Ryzen 5 16GB 512GB at £629.99, in stock. Model matches M1607KA-MB148W / 90NB15F1-M00A60 spec set.",
    "block_reason": None,
    "checked_at": NOW
}
p1["lowest_verified"] = {
    "price": 470.0,
    "currency": "GBP",
    "retailer_slug": "ao",
    "product_url": "https://ao.com/product/m1607kamb148w-asus-vivobook-16-m1607kamb148w-laptop--blue-107583-251.aspx",
    "retailers_checked": 7,
    "retailers_verified": 5,
    "retailers_verified_and_purchasable": 4,
    "computed_at": NOW
}
p1["last_checked"] = NOW
# No price change for this product (AO still £470)

# ── Product 2: 90NB10R2-M01820 (ASUS Vivobook M160) ────────────────────────
# ASUS UK Store: £499.99 → £549.99 (+£50, +10%) — MEANINGFUL PRICE INCREASE
# Argos: £499.99 (unchanged). New: Back to Office £584.99 (OOS), Quzo £518.01 (OOS), Box UK £469.99 (refurb OOS)
p2 = products["90NB10R2-M01820"]

# Update ASUS UK Store price
p2["retailers"]["asus-uk-store"]["price"] = 549.99
p2["retailers"]["asus-uk-store"]["last_verified"] = NOW
p2["retailers"]["asus-uk-store"]["checked_at"] = NOW
p2["retailers"]["asus-uk-store"]["evidence"] = "ASUS UK store page (web search + page fetch) shows Special Price GBP 549.99 / Regular Price GBP 549.99. Model M1605YA-MB601W, Part Number 90NB10R2-M01820 confirmed. Previously £499.99 on 2026-10-28."

# Add new retailers
p2["retailers"]["back-to-office"] = {
    "retailer": "Back to the Office",
    "retailer_slug": "back-to-office",
    "retailer_product_id": "MBM1605S00037",
    "listing_title": "ASUS Vivobook 16 M1605YA-MB601W AMD Ryzen 5 7430U 16GB 512GB SSD 16\" WUXGA - Silver",
    "product_url": "https://www.backtotheoffice.co.uk/asus-vivobook-16-m1605ya-mb601w-amd-ryzen-5-7430u-16gb-512gb-ssd-16-wuxga-silver-2133998",
    "price": 584.99,
    "currency": "GBP",
    "list_price": None,
    "price_type": "standard",
    "availability": "out_of_stock",
    "last_verified": NOW,
    "verification_status": "VERIFIED",
    "verification_method": "web_search_discovery",
    "verification_source": "https://www.google.com/search?q=ASUS+Vivobook+M160+90NB10R2-M01820+site:backtotheoffice.co.uk",
    "evidence": "Back to the Office listing confirms MBM1605S00037, Ryzen 5 7430U, 16GB, 512GB at £584.99. Out of stock.",
    "excluded_from_lowest_verified_reason": "availability is out_of_stock",
    "block_reason": None,
    "checked_at": NOW
}
p2["retailers"]["quzo"] = {
    "retailer": "Quzo",
    "retailer_slug": "quzo",
    "retailer_product_id": "M1605YA-MB601W",
    "listing_title": "ASUS Vivobook 16 M1605YA-MB601W",
    "product_url": "https://www.quzo.co.uk/product-page/asus-vivobook-16-m1605ya-mb601w",
    "price": 518.01,
    "currency": "GBP",
    "list_price": None,
    "price_type": "standard",
    "availability": "out_of_stock",
    "last_verified": NOW,
    "verification_status": "VERIFIED",
    "verification_method": "web_search_discovery",
    "verification_source": "https://www.google.com/search?q=ASUS+Vivobook+M160+90NB10R2-M01820+site:quzo.co.uk",
    "evidence": "Quzo listing shows M1605YA-MB601W at £518.01. Out of stock. Part number confirmed.",
    "excluded_from_lowest_verified_reason": "availability is out_of_stock",
    "block_reason": None,
    "checked_at": NOW
}
p2["retailers"]["box-uk"] = {
    "retailer": "Box UK",
    "retailer_slug": "box-uk",
    "retailer_product_id": "M1605YA-MB601W",
    "listing_title": "ASUS Vivobook 16 M1605YA-MB601W Refurbished",
    "product_url": "https://box.co.uk/90nb10r2-m01820-asus-vivobook-16-m1605",
    "price": 469.99,
    "currency": "GBP",
    "list_price": None,
    "price_type": "refurbished",
    "availability": "in_stock",
    "last_verified": NOW,
    "verification_status": "VERIFIED",
    "verification_method": "web_search_discovery",
    "verification_source": "https://www.google.com/search?q=ASUS+Vivobook+M160+90NB10R2-M01820+site:box.co.uk",
    "evidence": "Box UK refurbished unit at £469.99. Part number 90NB10R2-M01820 confirmed. Condition: refurbished.",
    "excluded_from_lowest_verified_reason": "price_type is refurbished — only new condition prices count toward lowest_verified",
    "block_reason": None,
    "checked_at": NOW
}

# Update lowest_verified (ASUS UK is now the only in-stock new-price retailer)
p2["lowest_verified"] = {
    "price": 549.99,
    "currency": "GBP",
    "retailer_slug": "asus-uk-store",
    "product_url": "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
    "retailers_checked": 8,
    "retailers_verified": 6,
    "retailers_verified_and_purchasable": 3,
    "computed_at": NOW
}

# Record price change
old_asus_price = 499.99
new_asus_price = 549.99
price_change = round(new_asus_price - old_asus_price, 2)
change_percent = round((price_change / old_asus_price) * 100, 1)

p2["price_changes"] = p2.get("price_changes", [])
p2["price_changes"].append({
    "from_price": old_asus_price,
    "to_price": new_asus_price,
    "change": price_change,
    "change_percent": change_percent,
    "detected_at": NOW,
    "reason": f"ASUS UK Store increased price from £{old_asus_price:.2f} to £{new_asus_price:.2f} (+£{price_change:.2f}, +{change_percent}%)"
})
p2["previous_price"] = old_asus_price
p2["current_price"] = new_asus_price
p2["price_change"] = price_change
p2["lowest_recorded_price"] = min(p2.get("lowest_recorded_price", 999), new_asus_price)
if new_asus_price > p2.get("highest_recorded_price", 0):
    p2["highest_recorded_price"] = new_asus_price
p2["last_checked"] = NOW

# ── Product 3: 6CH4H (Dell Inspiron 15 3530) ───────────────────────────────
# No confirmed price change. New: LaptopStation £409 (out of stock).
p3 = products["6CH4H"]
p3["retailers"]["laptopstation"] = {
    "retailer": "LaptopStation",
    "retailer_slug": "laptopstation",
    "retailer_product_id": "INSPIRON-15-3530-6CH4H",
    "listing_title": "Dell Inspiron 15 3530 Laptop - Intel Core i5-1334U 16GB 512GB SSD",
    "product_url": "https://www.laptopstation.co.uk/dell-inspiron-15-3530-laptop",
    "price": 409.0,
    "currency": "GBP",
    "list_price": None,
    "price_type": "standard",
    "availability": "out_of_stock",
    "last_verified": NOW,
    "verification_status": "VERIFIED",
    "verification_method": "web_search_discovery",
    "verification_source": "https://www.google.com/search?q=Dell+Inspiron+15+3530+6CH4H+site:laptopstation.co.uk",
    "evidence": "LaptopStation listing shows Dell Inspiron 15 3530 at £409.00. Out of stock / sold out.",
    "excluded_from_lowest_verified_reason": "availability is out_of_stock",
    "block_reason": None,
    "checked_at": NOW
}
p3["lowest_verified"] = {
    "price": 524.16,
    "currency": "GBP",
    "retailer_slug": "esupply",
    "product_url": "https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/",
    "retailers_checked": 4,
    "retailers_verified": 2,
    "retailers_verified_and_purchasable": 1,
    "computed_at": NOW
}
p3["last_checked"] = NOW

# ── Product 4: 3XGG3 (Dell 16 DC16251) ─────────────────────────────────────
# Already at £991.20 from last run. John Lewis confirmed at £999. No change.
p4 = products["3XGG3"]
p4["retailers"]["johnlewis"]["price"] = 999.0
p4["retailers"]["johnlewis"]["last_verified"] = NOW
p4["retailers"]["johnlewis"]["checked_at"] = NOW
p4["retailers"]["johnlewis"]["evidence"] = "John Lewis confirms Dell 16 DC16251 (MPN 3XGG3) at £999.00, in stock. Same price as prior check."
p4["retailers"]["dell-uk"]["price"] = 991.2
p4["retailers"]["dell-uk"]["last_verified"] = NOW
p4["retailers"]["dell-uk"]["checked_at"] = NOW
p4["retailers"]["dell-uk"]["evidence"] = "Dell UK confirms DC16251 at £991.20 (incl. delivery), in stock. Same as prior check."
p4["lowest_verified"] = {
    "price": 991.2,
    "currency": "GBP",
    "retailer_slug": "dell-uk",
    "product_url": "https://www.dell.com/en-uk/shop/laptops-2-in-1-pcs/dell-16-laptop/spd/dell-dc16251-laptop/cndc1625104?view=configurations",
    "retailers_checked": 4,
    "retailers_verified": 3,
    "retailers_verified_and_purchasable": 2,
    "computed_at": NOW
}
p4["last_checked"] = NOW

# ── Product 5: D8WA6EA#ABU (HP 15-fd1000nax) ──────────────────────────────
# John Lewis £699 unchanged. New: AO £849.
p5 = products["D8WA6EA#ABU"]
p5["retailers"]["ao"] = {
    "retailer": "AO",
    "retailer_slug": "ao",
    "retailer_product_id": "d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251",
    "listing_title": "HP 15-fd1000nax Laptop - Black",
    "product_url": "https://ao.com/product/d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251.aspx",
    "price": 849.0,
    "currency": "GBP",
    "list_price": None,
    "price_type": "standard",
    "availability": "in_stock",
    "last_verified": NOW,
    "verification_status": "VERIFIED",
    "verification_method": "direct_page_fetch",
    "verification_source": "https://ao.com/product/d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251.aspx",
    "evidence": "AO product page shows HP 15-fd1000nax (D8WA6EA#ABU) at £849.00, in stock. Same model as John Lewis listing.",
    "block_reason": None,
    "checked_at": NOW
}
p5["lowest_verified"] = {
    "price": 699.0,
    "currency": "GBP",
    "retailer_slug": "johnlewis",
    "product_url": "https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654",
    "retailers_checked": 5,
    "retailers_verified": 3,
    "retailers_verified_and_purchasable": 2,
    "computed_at": NOW
}
p5["last_checked"] = NOW

# ── Save products.json ──────────────────────────────────────────────────────
products_data["_updated_at"] = NOW
with open("data/products.json", "w") as f:
    json.dump(products_data, f, indent=2, ensure_ascii=False)
print("products.json updated")

# ── Add price history observations ──────────────────────────────────────────
def add_obs(manufacturer_part_number, product_id, product_name, retailer, retailer_slug,
            retailer_product_id, price, availability, product_url, evidence,
            change_from_prev=None, first_obs=False):
    global obs_counter
    obs_counter += 1
    obs = {
        "observation_id": f"obs_{TODAY.replace('-','')}_p{obs_counter}",
        "observed_at": NOW,
        "manufacturer_part_number": manufacturer_part_number,
        "product_id": product_id,
        "product": product_name,
        "retailer": retailer,
        "retailer_slug": retailer_slug,
        "retailer_product_id": retailer_product_id,
        "price": price,
        "currency": "GBP",
        "availability": availability,
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch" if "direct_page" in evidence else "web_search_discovery",
        "verification_source": product_url,
        "product_url": product_url,
        "evidence": evidence,
        "first_observation_for_product": first_obs
    }
    if change_from_prev:
        obs["change_from_previous"] = change_from_prev
    observations.append(obs)

# Product 1: Argos new entry
add_obs("90NB15F1-M00A60", "asus-vivobook-16-m1607ka-mb148w",
        "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
        "Argos", "argos", "7741159", 629.99, "in_stock",
        "https://www.argos.co.uk/product/7741159",
        "Argos listing 7741159: ASUS Vivobook AI 16in Ryzen 5 16GB 512GB at £629.99, in stock.")

# Product 2: ASUS UK Store price increase
add_obs("90NB10R2-M01820", "asus-vivobook-16-m1605ya-mb601w",
        "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
        "ASUS UK Store", "asus-uk-store", "90NB10R2-M01820", 549.99, "in_stock",
        "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
        "ASUS UK store page: Special Price GBP 549.99. Model M1605YA-MB601W, Part 90NB10R2-M01820. Previously £499.99 on 2026-10-28.",
        change_from_prev={"from": 499.99, "to": 549.99, "change": 50.0, "percent": 10.0})

# Product 2: New retailers (all out of stock)
add_obs("90NB10R2-M01820", "asus-vivobook-16-m1605ya-mb601w",
        "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
        "Back to the Office", "back-to-office", "MBM1605S00037", 584.99, "out_of_stock",
        "https://www.backtotheoffice.co.uk/asus-vivobook-16-m1605ya-mb601w-amd-ryzen-5-7430u-16gb-512gb-ssd-16-wuxga-silver-2133998",
        "Back to the Office: £584.99, out of stock. Part MBM1605S00037.")
add_obs("90NB10R2-M01820", "asus-vivobook-16-m1605ya-mb601w",
        "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
        "Quzo", "quzo", "M1605YA-MB601W", 518.01, "out_of_stock",
        "https://www.quzo.co.uk/product-page/asus-vivobook-16-m1605ya-mb601w",
        "Quzo: £518.01, out of stock. Part M1605YA-MB601W.")
add_obs("90NB10R2-M01820", "asus-vivobook-16-m1605ya-mb601w",
        "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
        "Box UK", "box-uk", "M1605YA-MB601W", 469.99, "in_stock",
        "https://box.co.uk/90nb10r2-m01820-asus-vivobook-16-m1605",
        "Box UK refurbished: £469.99, in stock. Part M1605YA-MB601W. Refurbished condition.")

# Product 3: LaptopStation new (out of stock)
add_obs("6CH4H", "dell-inspiron-15-3530-6ch4h",
        "Dell Inspiron 15 3530",
        "LaptopStation", "laptopstation", "INSPIRON-15-3530-6CH4H", 409.0, "out_of_stock",
        "https://www.laptopstation.co.uk/dell-inspiron-15-3530-laptop",
        "LaptopStation: Dell Inspiron 15 3530 at £409.00, sold out.")

# Product 5: AO new discovery
add_obs("D8WA6EA#ABU", "hp-15-fd1000nax-d8wa6ea-abu",
        "HP 15-fd1000nax",
        "AO", "ao", "d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251", 849.0, "in_stock",
        "https://ao.com/product/d8wa6eaabu-hp-15fd1000nax-laptop--black-112548-251.aspx",
        "AO product page: HP 15-fd1000nax (D8WA6EA#ABU) at £849.00, in stock.")

history_data["observations"] = observations
with open("data/price-history.json", "w") as f:
    json.dump(history_data, f, indent=2, ensure_ascii=False)
print("price-history.json updated")

print(f"\n=== SUMMARY ===")
print(f"Products checked: 5")
print(f"Price changes: 1")
print(f"  - ASUS Vivobook M160 (90NB10R2): ASUS UK Store £499.99 → £549.99 (+£50.00, +10.0%)")
print(f"New retailers discovered: 6")
print(f"Meaningful alerts: 1 (price increase ≥£5 and ≥10%)")
