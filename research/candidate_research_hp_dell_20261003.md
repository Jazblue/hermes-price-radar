# Candidate Research — HP and Dell Expansion to Max 8 Products

Date: 2026-10-03
Status: CANDIDATE EVIDENCE ONLY. Not ranked, not selected, not added to production.
No production file modified. No commit. No push.

Existing tracked products confirmed untouched: `90NB15F1-M00A60` (ASUS Blue, lowest GBP549.99
@ asus-uk-store) and `90NB10R2-M01820` (ASUS Silver, lowest GBP499.99 @ asus-uk-store).
HEAD still `39cb525`, tracked working tree clean.

Target: up to 3 HP + 3 Dell = max 8 total.

---

## HP candidates

### HP-1: HP 15-fd1010nax — Intel Core 5 120U, 16GB, 512GB
| Field | Value |
|---|---|
| Brand | HP |
| Exact model | 15-fd1010nax |
| Manufacturer part number | **D8WB0EA#ABU** (EAN 0821844531426) |
| CPU | Intel Core 5 120U (10 cores / 12 threads, 1.4GHz P-core base, boost 5GHz) |
| RAM | 16GB DDR4-3200 (1 x 16GB SO-DIMM) |
| SSD | 512GB PCIe NVMe M.2 |
| Screen | 15.6in HD 1366x768, anti-glare, 250 nits |
| UK price seen | GBP 1,140.99 (Direct Computers, ex-VAT 950.83) |
| Retailer | Direct Computers |
| URL | https://directcomputers.co.uk/products/15-fd1010nax-c5-120u-16gb-512gb-w11h |
| Verification | VERIFIED (body read at source; SKU, barcode, full spec table) |

**Why valid exact match:** Part number `D8WB0EA#ABU` is printed on the retailer page with
matching EAN. Full spec table confirms every target field.

**Conflicts / uncertainty — SIGNIFICANT:**
- Retailer shows **"Unavailable"** despite displaying GBP 1,140.99.
- Price across retailers for this identical part number: GBP 499.99 (idealo, "from"),
  GBP 699.99-849.00 (Shopping.co.uk), GBP 915.47 (Avoira), GBP 951.61 (Expandeo),
  GBP 1,022.99 / GBP 1,140.99 (Direct Computers). **Spread of roughly 2.3x.**
- Likely a business/bulk SKU priced above consumer mainstream, or thin reseller margins.
- **Fails the GBP400-800 mainstream criterion** on every verified figure.

### HP-2: HP 15-fd0001na — Intel Core i5-1334U, 16GB, 512GB
| Field | Value |
|---|---|
| Brand | HP |
| Exact model | 15-fd0001na |
| Manufacturer part number | **Not captured** — model string only |
| CPU | Intel Core i5-1334U (13th Gen Raptor Lake) |
| RAM | 16GB |
| SSD | 512GB |
| Screen | 15.6in (resolution not captured) |
| UK price seen | GBP 479.00 |
| Retailer | Argos (product 8172112) |
| URL | https://www.argos.co.uk/product/8172112 |
| Verification | UNVERIFIED (search snippet + PriceRunner corroboration only) |

**Why valid match:** Spec set and model string agree across Argos and PriceRunner.

**Conflicts / uncertainty:** No manufacturer part number obtained, which fails your
"identifiable exact part number" criterion. Argos is BLOCKED for us (HTTP 403), so this
price cannot be independently verified by fetch — same trap as the ASUS listings.

### HP-3: HP 250 G9 6S6S9EA — Intel Core i5-1235U, 16GB, 512GB
| Field | Value |
|---|---|
| Brand | HP |
| Exact model | HP 250 G9 |
| Manufacturer part number | **6S6S9EA#ABU** |
| CPU | Intel Core i5-1235U (12th Gen, 10 cores / 12 threads, up to 4.6GHz) |
| RAM | 16GB DDR4 |
| SSD | 512GB |
| Screen | 15.6in Full HD |
| UK price seen | GBP 539.00 (PriceRunner, 1 store) / GBP 588.50 (2 stores) |
| Retailer | Laptop Outlet, Technoworld |
| URL | https://www.laptopoutlet.co.uk/hp-250-g9-15-6-full-hd-laptop-i5-1235u-16gb-ddr4-ram-512gb-ssd-windows-11-pro-6s6s9ea-abu-ag.html |
| Verification | UNVERIFIED (part number corroborated by HP's own support site and two retailers; no direct price fetch succeeded) |

**Why valid match:** Part number `6S6S9EA#ABU` confirmed on HP's official support site
(`support.hp.com/gb-en/product/troubleshooting/...model/2101136070?sku=6S6S9EA`) and on
retailer listings.

**Conflicts / uncertainty:** Near-identical sibling `6S6E8EA` also exists — different part
number, must not be conflated. Note the Laptop Outlet URL slug ends `-ag`, a suffix this
retailer uses for **refurbished** stock; the listed spec block says Windows 11 Pro but
condition is not clear from the snippet. Windows **Pro** rather than Home, which may not
match your intent. Price is a PriceRunner aggregate across 1-2 stores, not a direct read.

---

## Dell candidates

### Dell-1: Dell Inspiron 15 3530 — Intel Core i5-1334U, 16GB, 512GB
| Field | Value |
|---|---|
| Brand | Dell |
| Exact model | Inspiron 15 3530 |
| Manufacturer part number | **6CH4H** (Dell SKU) |
| CPU | Intel Core i5-1334U (13th Gen Raptor Lake, 10 cores / 12 threads, up to 4.6GHz) |
| RAM | 16GB DDR4-2666 (2 x 8GB SO-DIMM) |
| SSD | 512GB PCIe 3.0/4.0 x4 NVMe M.2 22x80 |
| Screen | 15.6in FHD 1920x1080 IPS, 120Hz, 250 nits |
| UK price seen | **GBP 524.16** (eSupply); GBP 599.23 (Quzo via e-Catalog) |
| Retailer | eSupply (5Tech Ltd group) |
| URL | https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/ |
| Verification | **VERIFIED** (body read at source; SKU 6CH4H + full spec table + cart present) |

**Why valid match:** Page states "Dell SKU: 6CH4H" and the full spec table matches every
target field exactly. Stock control and Add to Cart present.

**Conflicts / uncertainty:** Windows **11 Pro** (business SKU), not Home. Second retailer
(Quzo) quotes GBP 599.23 vs GBP 524.16. Currys Business lists the same 6CH4H but shows
out of stock. Colour listed as Carbon Black on eSupply, though e-Catalog describes the
family as aluminium.

### Dell-2: Dell Latitude 3540 — Intel Core i5-1235U, 16GB, 512GB
| Field | Value |
|---|---|
| Brand | Dell |
| Exact model | Latitude 15 3540 |
| Manufacturer part number | **29YN0** (EAN 5397184863916) |
| CPU | Intel Core i5-1235U (12th Gen Alder Lake, 10 cores / 12 threads, up to 4.4GHz) |
| RAM | 16GB DDR4-3200 |
| SSD | 512GB PCIe 4.0 x4 NVMe M.2 |
| Screen | 15.6in FHD 1920x1080 IPS, 60Hz, anti-glare, 250 nits |
| UK price seen | GBP 551.10 (Quzo); GBP 566.00 (Athema); GBP 733.06 ex-VAT / 879.67 inc (Technoworld) |
| Retailer | Quzo (via compareaprice), Athema Services, Technoworld |
| URL | https://www.athema.co.uk/dell-lat-3540-i5-16gb512g-29yn0-wc01-pr-3699479.html |
| Verification | UNVERIFIED (part number + EAN confirmed; all price sources are aggregators or unverified) |

**Why valid match:** Part number 29YN0 and EAN 5397184863916 consistent across Technoworld,
e-Catalog and compareaprice.

**Conflicts / uncertainty — heaviest price spread of the six:**
- GBP 551.10 (Quzo, aggregator) vs GBP 566.00 (Athema) vs GBP 733.06 (Technoworld ex-VAT).
- **compareaprice JSON-LD explicitly marks the Quzo offer `schema.org/OutOfStock`.**
- Technoworld page shows "In Stock: N" and "Out of stock".
- Dell UK's own Latitude 3540 product page now reads **"Unavailable"** and redirects to the
  newer Dell Pro 14 line — this model is being discontinued.
- Windows 11 Pro, business line.

### Dell-3: Dell Inspiron 15 3520 — Intel Core i5-1235U, 16GB, 512GB
| Field | Value |
|---|---|
| Brand | Dell |
| Exact model | Inspiron 15 3520 |
| Manufacturer part number | **Not captured** — model string only |
| CPU | Intel Core i5-1235U (12th Gen Alder Lake, 10 cores / 12 threads, up to 4.4GHz) |
| RAM | 16GB DDR4 |
| SSD | 512GB PCIe NVMe M.2 |
| Screen | 15.6in FHD 1920x1080 IPS, **120Hz**, 250 nits |
| UK price seen | GBP 699.00 |
| Retailer | Amazon UK (per third-party review site) |
| URL | https://www.dell.com/en-uk/shop/laptops-2-in-1-pcs/inspiron-15-laptop/spd/inspiron-15-3520-laptop |
| Verification | UNVERIFIED (Dell UK page says "This product is no longer available"; price is from a third-party review article) |

**Why valid match:** Spec set matches the target configuration consistently across sources.

**Conflicts / uncertainty:** No manufacturer part number obtained — fails your criterion.
Dell UK lists the model as **no longer available**, steering to Dell 15 DC15250 from
GBP 649.00. The GBP 699.00 comes from a review article, not the retailer, and it names
Windows 11 Home while Currys Business lists a Win 11 Pro variant of the same model —
configuration ambiguity across retailers. Also note the same model appears with 8GB and
different storage in many listings.

---

## Rejected during research

| Item | Reason |
|---|---|
| HP ENVY 14-eb0505na (3Y0L5EA#ABU) | Laptop Outlet SKU is `RFB-` prefixed — **Certified Refurbished**, and Out of Stock |
| HP ENVY x360 16-ad0002na | Only 8GB RAM; John Lewis shows out of stock |
| HP OmniBook 5 (AMD Ryzen AI 5 340) | 16GB but **1TB** not 512GB; John Lewis out of stock |
| HP 15-fc0049na | John Lewis "No longer available online" |
| HP Victus 16-e0071na | RTX 3050 gaming SKU, Servers Direct, "no longer available" |
| HP 15-fc0046na | Only **8GB** RAM |
| HP 15-fc0083na | Only **8GB** RAM / 256GB |
| HP OmniBook 5 Sky Blue (1TB) | 1TB storage, out of stock |
| Dell Inspiron 15 3535 Ryzen 5 7520U | Only **8GB** RAM |
| Dell Latitude 3440 NJY3W | 16GB but only **256GB** SSD |
| Dell Latitude 3440 (computerdealsdirect) | **Spanish keyboard**, and prices in USD not GBP |
| Dell Inspiron 14 (laptopstation) | **Refurbished** ("Refurbished to Dell's highest standards") |
| Dell Latitude 3540 (greengreenstore) | **Refurbished Grade C**, 256GB, screen "grade B" |
| Dell Inspiron 15 3520 (Amazon B0F2VQ5T44) | Windows 11 **Pro**, GBP 869.00 — different config to Dell-3 |
| ASUS / Acer / other brands | Out of scope for this expansion |

---

## Summary

| ID | Brand | Model | Part number | CPU | RAM/SSD | Price seen | Verification |
|---|---|---|---|---|---|---|---|
| HP-1 | HP | 15-fd1010nax | D8WB0EA#ABU | Core 5 120U | 16/512 | GBP 1,140.99 (unavailable) | VERIFIED |
| HP-2 | HP | 15-fd0001na | — | Core i5-1334U | 16/512 | GBP 479.00 | UNVERIFIED |
| HP-3 | HP | 250 G9 | 6S6S9EA#ABU | Core i5-1235U | 16/512 | GBP 539.00 | UNVERIFIED |
| Dell-1 | Dell | Inspiron 15 3530 | 6CH4H | Core i5-1334U | 16/512 | GBP 524.16 | **VERIFIED** |
| Dell-2 | Dell | Latitude 3540 | 29YN0 | Core i5-1235U | 16/512 | GBP 551.10 | UNVERIFIED |
| Dell-3 | Dell | Inspiron 15 3520 | — | Core i5-1235U | 16/512 | GBP 699.00 | UNVERIFIED |

**Fully verified and available: 1 of 6** (Dell-1, Dell Inspiron 15 3530).

**Caveats worth weighing before selection:**
- HP-1 and Dell-2 carry **manufacturer part numbers** but both have severe price spreads
  (2.3x and 1.3x respectively) and availability problems.
- HP-2 and Dell-3 have **no manufacturer part number**, which is the identity anchor the
  whole schema is built on — both would fail tracking on principle.
- HP-2's only price source is **Argos**, which is BLOCKED for us.
- HP-3, Dell-2 and Dell-3 are Windows 11 **Pro** (business) rather than Home.
- Dell-3 is being discontinued by Dell; Dell-2 already shows "Unavailable" on Dell UK.
- None of these are gaming SKUs, which is why RTX/RTX-4050 models were excluded as
  out-of-scope for mainstream pricing.