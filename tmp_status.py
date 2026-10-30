import json
d = json.load(open('data/products.json'))
prods = d['products'] if 'products' in d else d
for pid, p in prods.items():
    retail = p.get('retailers', {})
    lv = p.get('lowest_verified')
    title = p.get('marketing_title', '?')[:70]
    print(f"{pid} | {title} | retailers={list(retail.keys())}")
    for rs, r in retail.items():
        print(f"    {rs}: {r.get('price')} GBP | avail={r.get('availability')} | last_verified={r.get('last_verified')}")
    if lv:
        print(f"    LOWEST: {lv.get('price')} @ {lv.get('retailer_slug')} | verified={lv.get('retailers_verified')}/{lv.get('retailers_checked')} computed_at={lv.get('computed_at')}")
print("TOTAL PRODUCTS:", len(prods))
