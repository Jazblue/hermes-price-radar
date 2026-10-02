# Rejected Matches — Durable Research Record

Date: 2026-10-03
Status: research/discovery evidence. NOT price observations. Deliberately not stored in
data/price-history.json.

Rule these exist to enforce: a near-miss that was rejected once must not be rediscovered and
re-evaluated every run, and must never silently become a tracked price if it later changes.

---

## Rejected for 90NB10R2-M01820 (ASUS Vivobook 16 M1605YA-MB601W, Silver)

Tracked spec: Ryzen 5 7430U / 16GB DDR4 / 512GB / Cool Silver / Win 11 Home

| Retailer | Model | Price seen | Spec delta | URL |
|---|---|---|---|---|
| AO | M1605YA-MB270W | £479 | Ryzen **7**, **8GB** RAM | ao.com/product/m1605yamb270w-asus-vivobook-16-laptop-black-99132-251.aspx |
| Mesh Computers | M1605YA-MB296W | £699 | Ryzen 7 7730U, **40GB** RAM, **1TB** SSD, Win 11 **Pro** | meshcomputers.com/...KEY=4379818 |
| Laptop Outlet | M1605YA-MB456W | — | Ryzen 7 7730U, **1TB** SSD, condition: **Refurbished - Excellent** | laptopoutlet.co.uk/asus-vivobook-16-in-m1605ya-mb456w-ag.html |
| Scan | M1605NAQ-MB077W | — | Ryzen 5 **150** — different generation. Also **End Of Life** | scan.co.uk/products/16-asus-vivobook-16-m1605naq-silver-fhd-ryzen-5-150-... |

## Rejected for 90NB15F1-M00A60 (ASUS Vivobook 16 M1607KA-MB148W, Blue)

Tracked spec: Ryzen AI 5 330 / 16GB DDR5 / 512GB / Quiet Blue

| Retailer | Model | Price seen | Spec delta | URL |
|---|---|---|---|---|
| Laptopstation | none stated | £389 | Generic "Ryzen 5 3.3-4.55GHz (150)", **no part number published**. Also **Out of Stock** | laptopstation.co.uk/products/asus-laptop-vivobook-16-amd-ryzen-5-16gb-ddr5-... |

---

## Watch list (not rejected — matching is plausible but unconfirmed)

| Retailer | Product | Why unresolved | URL |
|---|---|---|---|
| eBay | M1607KA-MB148W | Marketplace, no spec detail captured | ebay.co.uk/itm/198668317021 |
| e-Catalog UK | M1605YA-MB601W | Aggregator listing £429.99–£592.00 range across 8 stores — range, not a price | e-catalog.co.uk/ASUS-VIVOBOOK-16-M1605YA.htm |
| PriceSpy | both products | Comparison site. Blue showed £425.00–£499.00 range, inconsistent with Argos' own pages | pricespy.co.uk/product.php?p=15446850 |
| PriceRunner | Blue | Comparison site showing four prices incl. £749.99 | pricerunner.com/pl/27-3434872443/... |
| Icecat / laptoparena | M1607KA-MB148W | Catalogue aggregator; lists CPU as Ryzen AI 5 **340**, conflicting with ASUS UK's 330 | icecat.biz/en/p/asus/90nb15f1-m00a60/... |
| Very | ASUS laptops | Brand page surfaced in results, no model-level price captured | very.co.uk |

These are re-examined only if a direct page fetch succeeds. None may contribute a price.

---

## Note on the Blue CPU conflict

The Icecat/laptoparena listing gives Ryzen AI 5 **340** while ASUS UK's own store gives **330**.
This is recorded as an unresolved `spec_conflicts` entry on the product in data/products.json,
not resolved here. Same part number (90NB15F1-M00A60) appears in both, which is strong evidence
they are the same SKU with an aggregator error — but that is an inference, not a verified fact,
so the conflict stays open rather than being silently closed.