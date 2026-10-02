# Alternative Retailer Price Discovery — ASUS Test Dataset

Date: 2026-10-03
Method: web_search (Exa) for discovery + web_extract for direct page reads on retailer URLs.
No Playwright. No anti-bot evasion. No production files touched.

---

## Critical model-identification finding

The two tracked products were being matched on Argos marketing titles only. Both resolve
to exact ASUS model numbers:

| Tracked product | Argos marketing title | Exact ASUS model | Part number | Specs |
|---|---|---|---|---|
| asus-vivobook-ai-16in-...-blue | ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue | **M1607KA-MB148W** | 90NB15F1-M00A60 | Ryzen AI 5 330, 16GB DDR5, 512GB, Quiet Blue |
| asus-vivobook-m160-...-silver | ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver | **M1605YA-MB601W** | 90NB10R2-M01820 | Ryzen 5 7430U, 16GB DDR4, 512GB, Cool Silver |

The Argos M160 page itself states "Model number: M1605YA-MB601W" (seen in the indexed
page text). The Blue product's model number was not visible in Argos text, but
PriceRunner/PriceSpy listings for the identical spec set (Ryzen AI 5 330 / 16GB DDR5 /
512GB / Blue) consistently cite M1607KA-MB148W — matching the ASUS UK store listing.

**Consequence:** searching by Argos's marketing title is unreliable. Part numbers are the
correct join key.

---

## PRODUCT 1 — M1607KA-MB148W (Argos "Vivobook AI 16in ... Blue")

### VERIFIED — ASUS UK Store
- Retailer: ASUS UK Store (uk.store.asus.com, operated by authorised reseller FiveTech Ltd)
- Model: M1607KA-MB148W / Part 90NB15F1-M00A60
- Price shown: **£549.99** ("Special Price", regular £749.99, "You save £200")
- Availability: Add to Cart present, delivery 2-3 business days
- URL: https://uk.store.asus.com/asus-vivobook-16-m1607-copilot-pc-286177081-90nb15f1-m00a60.html
- Page fetched directly, full spec table read. Clearly current and public.
- Verification: **VERIFIED** (manufacturer's own UK store, page read at source)

### Exact match, different retailer — Laptop Outlet
- Retailer: Laptop Outlet (laptopoutlet.co.uk)
- Model: M1607KA-MB148W / SKU M1607KA-MB148W / Part 90NB15F1-M00A60
- Price shown: **£619.99 inc. VAT** (ex-VAT £516.66; was £749.99, "Save £130")
- Availability: **Out of Stock**
- URL: https://www.laptopoutlet.co.uk/asus-vivobook-16-90nb15f1-m00a60.html
- Page fetched directly, spec table confirms same model number and part number.
- Verification: **VERIFIED price, but NOT purchasable (out of stock)** — must not be
  used as an available-price or lowest-price candidate.

### Exact match, listed — AO (not verifiable)
- Retailer: AO
- Model: M1607KA-MB148W (from URL slug)
- URL: https://ao.com/product/m1607kamb148w-asus-vivobook-16-m1607kamb148w-laptop--blue-107583-251.aspx
- Page fetch failed (CRAWL_UNKNOWN_ERROR). No price captured.
- Verification: **UNVERIFIED** — discovery only.

### Argos own price is inconsistent across its own pages
Not a verification, but material — three different figures for the same Blue product:
- Product page snippet: **£549.00**
- /sd/asus-vivobook/ category page: **£499.00**
- /browse/technology/laptops.../laptops listing: **£629.99**
- PriceSpy snippet: "Lowest: £425.00 | Highest: £499.00"
None of these can be confirmed without fetching the page, which is 403-blocked. The stored
£549.00 in data/products.json is therefore not corroborated and may be stale.

---

## PRODUCT 2 — M1605YA-MB601W (Argos "Vivobook M160 16in R5 ... Silver")

### VERIFIED — ASUS UK Store
- Retailer: ASUS UK Store (uk.store.asus.com, FiveTech Ltd)
- Model: M1605YA-MB601W / Part 90NB10R2-M01820
- Price shown: **£499.99** ("Special Price", regular £549.99, "Save £50")
- Availability: Add to Cart present, delivery 2-3 business days
- URL: https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html
- Page fetched directly, full spec table read.
- Verification: **VERIFIED** (manufacturer's own UK store, page read at source)

Note this is £49.01 BELOW the £549.00 currently stored for this product in
data/products.json — a potential real drop that is currently being missed.

### Partial matches only (different configurations — NOT the same product)
| Retailer | Model | Spec delta | Price | URL |
|---|---|---|---|---|
| AO | M1605YA-MB270W | Ryzen **7**, 8GB | £479 | ao.com/product/m1605yamb270w-... |
| Mesh Computers | M1605YA-MB296W | Ryzen 7 7730U, 40GB, 1TB | £699 | meshcomputers.com |
| Laptop Outlet | M1605YA-MB456W | Ryzen 7 7730U, 16GB, 1TB, **Refurbished** | not captured | laptopoutlet.co.uk |
| Scan | M1605NAQ-MB077W | Ryzen 5 **150** (different gen) | **End of Life** | scan.co.uk |

All are same chassis family, wrong specification. **Do not record these against the
tracked product.**

### Amazon UK listing (not verified)
- Model: M1605YA-MB601W per product detail table (RAM listed inconsistently as 16GB in
  title and 8GB in the spec table on the same snippet — Amazon's own metadata is sloppy)
- Price shown: "New & Used (6) from £398.99"
- URL: https://www.amazon.co.uk/ASUS-Vivobook-M1605YA-5-7430U-Windows/dp/B0BXKM1PQN
- Not fetched directly. Marketplace/aggregated "from" price.
- Verification: **UNVERIFIED** — do not treat "from £398.99" as the current price.

---

## Summary

| | Product 1 (Blue) | Product 2 (Silver) |
|---|---|---|
| Exact model | M1607KA-MB148W | M1605YA-MB601W |
| Retailers discovered | 4 (ASUS UK, Laptop Outlet, AO, Argos) | 5 (ASUS UK, AO, Mesh, Laptop Outlet, Scan, Amazon) |
| Retailers price-verified | 1 (ASUS UK £549.99) | 1 (ASUS UK £499.99) |
| Exact match but unavailable | 1 (Laptop Outlet £619.99, out of stock) | 0 |
| Lowest VERIFIED price | **£549.99** (ASUS UK) | **£499.99** (ASUS UK) |
| Argos current price | UNVERIFIED (403) | UNVERIFIED (403) |

## Method findings for the skill

1. **uk.store.asus.com is readable** — no bot protection, full spec table, price in main
   HTML. Best available source for ASUS products.
2. **laptopoutlet.co.uk is readable** — full spec table with SKU and part number.
   Must check stock status; "out of stock" prices must be excluded from lowest-price calc.
3. **Argos is unreadable** (403 at edge, Akamai). Confirmed again by direct curl and Jina.
4. **Part number is the reliable join key**, not marketing title. Argos titles ("M160",
   "AI 16in") do not map to model numbers without reading the page.
5. **Argos' own pages disagree with each other** on price for the same SKU. Any future Argos
   entry should be treated as low-confidence even if access is restored.
6. ao.com fetch failed via this backend — needs a separate check if AO is to be included.