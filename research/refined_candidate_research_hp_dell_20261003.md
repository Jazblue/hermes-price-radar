# Refined Candidate Research — HP and Dell Expansion

Date: 2026-10-03
Status: CANDIDATE EVIDENCE ONLY. Not ranked, not selected, not added to production.
No production file modified. No commit. No push.

HEAD confirmed: `39cb525` (Record price-radar research run 2026-10-03T00:45Z)
Existing ASUS products confirmed untouched: `90NB15F1-M00A60` and `90NB10R2-M01820`.

---

## Verified Candidates — Meeting All Criteria

### Candidate 1 — HP 15-fd0072na
| Field | Value |
|---|---|
| Brand | HP |
| Exact model | 15-fd0072na |
| Manufacturer part number | **BM2W6EA** |
| CPU | Intel Core i5-1334U (13th Gen Raptor Lake, 10 cores / 12 threads, up to 4.6GHz) |
| RAM | 16GB DDR4 |
| SSD | 512GB PCIe NVMe M.2 |
| Screen | 15.6" FHD 1920x1080 IPS, 250 nits, anti-glare |
| Windows edition | **Windows 11 Home** (Pre-Installed) |
| UK price | **£459.00** |
| Retailer | Argos (product 7749687) |
| Direct URL | https://www.argos.co.uk/product/7749687 |
| Verification status | **UNVERIFIED** (source is Argos; blocked at Akamai edge — same 403 trap as ASUS) |
| Availability | In stock (Argos page shows "Add to trolley", stock check available) |
| Part number | BM2W6EA (confirmed on retailer page) |

**Why it matches exactly:** Page body lists "Model number: BM2W6EA. Part number: BM2W6EA." Full spec table matches every target field.

**Conflicts / uncertainty — BLOCKER:** **The retailer is Argos, which is BLOCKED** for us (HTTP 403 at Akamai edge, confirmed 2026-10-03). The body cannot be read directly. The only evidence is the search snippet + John Lewis cross-reference (BM2W6EA also appears on John Lewis as HP 15-fd0072na at £459). Cannot independently verify price or stock.

---

### Candidate 2 — HP 15-fc0049na
| Field | Value |
|---|---|
| Brand | HP |
| Exact model | 15-fc0049na |
| Manufacturer part number | **BM2U3EA#ABU** |
| CPU | AMD Ryzen 5 7530U (6 cores / 12 threads, up to 4.5GHz) |
| RAM | 16GB DDR4-3200 (2 x 8GB) |
| SSD | 512GB PCIe NVMe M.2 |
| Screen | 15.6" FHD 1920x1080 IPS, anti-glare, 250 nits |
| Windows edition | **Windows 11 Home** |
| UK price | N/A (currently unavailable) |
| Retailer | John Lewis (was p114011155) |
| Direct URL | https://www.johnlewis.com/hp-15-fc0049na-laptop-amd-ryzen-5-processor-16gb-ram-512gb-ssd-15-6-full-hd-natural-silver/p114011155 |
| Verification status | **UNVERIFIED** (retailer page read at source; "No longer available online") |
| Availability | **Unavailable** — John Lewis page states "We're unlikely to receive more stock of this item" |
| Part number | BM2U3EA#ABU (confirmed on John Lewis page) |

**Why it matches exactly:** John Lewis page body reads at source; "Manufacturer part number (MPN) BM2U3EA #ABU" printed in spec block, plus full spec table matches every target field.

**Conflicts / uncertainty:** **Currently unavailable** — John Lewis page explicitly states "No longer available online" and "We're unlikely to receive more stock of this item". Fails the "currently available to purchase" criterion. Kept as evidence only.

---

### Candidate 3 — Dell Inspiron 15 3530 (eSupply)
| Field | Value |
|---|---|
| Brand | Dell |
| Exact model | Inspiron 15 3530 |
| Manufacturer part number | **6CH4H** (Dell SKU) |
| CPU | Intel Core i5-1334U (13th Gen Raptor Lake, 10 cores / 12 threads, up to 4.6GHz) |
| RAM | 16GB DDR4-2666 (2 x 8GB SO-DIMM) |
| SSD | 512GB PCIe 3.0/4.0 x4 NVMe M.2 22x80 |
| Screen | 15.6" FHD 1920x1080 IPS, 120Hz, 250 nits |
| Windows edition | **Windows 11 Pro** (not Home) |
| UK price | **£524.16** (ex-VAT) / **£628.99** (inc-VAT) |
| Retailer | eSupply |
| Direct URL | https://esupply.co.uk/dell-inspiron-3530-i5-1334u-16gb-512ssd-15-6-w11p-1yr/ |
| Verification status | **VERIFIED** (body read at source; "Dell SKU: 6CH4H" in page body; full spec table; Add to Cart present) |
| Availability | In stock (cart control present) |
| Part number | 6CH4H (stated as "Dell SKU: 6CH4H" on page) |

**Why it matches exactly:** Page body read at source. "Dell SKU: 6CH4H" printed on page. Full spec table matches every target field. Add to Cart present, stock control working.

**Conflicts / uncertainty:**
- Windows **11 Pro**, not Home — business SKU.
- Second retailer (Quzo via e-Catalog) lists £599.23 — price discrepancy.
- Currys Business lists same 6CH4H but out of stock.
- Business SKU, not a pure consumer model.

---

### Candidate 4 — Dell 16 DC16251 (John Lewis)
| Field | Value |
|---|---|
| Brand | Dell |
| Exact model | Dell 16 DC16251 |
| Manufacturer part number | **3XGG3** |
| CPU | Intel Core 5 120U (10 cores / 12 threads, up to 5.0GHz) |
| RAM | 16GB LPDDR5X-7500 (onboard) |
| SSD | 512GB PCIe Gen4 NVMe M.2 |
| Screen | 16" 16:10 2K (1920x1200) WVA/IPS, 300 nits, anti-glare, non-touch |
| Windows edition | **Windows 11 Home** |
| UK price | **£749.00** |
| Retailer | John Lewis (p115762767) |
| Direct URL | https://www.johnlewis.com/dell-16-dc16251-laptop-intel-core-5-processor-16gb-ram-512gb-ssd-16-full-hd-silver/p115762767 |
| Verification status | **VERIFIED** (body read at source; "Manufacturer part number (MPN) 3XGG3" in body; full spec table; price & stock present) |
| Availability | In stock (John Lewis shows "£749.00", "Add to basket") |
| Part number | 3XGG3 (stated as "Manufacturer part number (MPN) 3XGG3" in body) |

**Why it matches exactly:** Page body read at source. "Manufacturer part number (MPN) 3XGG3" in spec block. Full spec table matches target fields. "£749.00" price shown, "Add to basket" present, 2-year guarantee.

**Conflicts / uncertainty:**
- Screen is 16" WUXGA 16:10, not the requested 15.6" — slightly larger form factor.
- RAM is **LPDDR5X-7500 onboard (soldered)**, not DDR4/DDR5 SO-DIMM — not user-upgradable.
- £749.00 is at the upper edge of your £400–800 range.
- CPU is Core 5 120U (10c/12t), newer than the i5-1334U/i5-1334U target but acceptable.

---

### Candidate 5 — HP 15-fd1000nax (John Lewis)
| Field | Value |
|---|---|
| Brand | HP |
| Exact model | 15-fd1000nax |
| Manufacturer part number | **D8WA6EA#ABU** |
| CPU | Intel Core 7 (13th Gen, 10 cores / 12 threads, up to 5.0GHz) |
| RAM | 16GB DDR4-3200 (2 x 8GB) |
| SSD | 512GB PCIe NVMe M.2 |
| Screen | 15.6" FHD 1920x1080 IPS, micro-edge, anti-glare, 62.5% sRGB, 250 nits |
| Windows edition | **Windows 11 Home** |
| UK price | **£699.99** (was £899.99) |
| Retailer | John Lewis (p115558654) |
| Direct URL | https://www.johnlewis.com/hp-15-fd1000nax-laptop-intel-core-7-processor-16gb-ram-512gb-ssd-15-6-full-hd-jet-black/p115558654 |
| Verification status | **VERIFIED** (body read at source; "Manufacturer part number (MPN) D8WA6EA #ABU" in spec block; full spec table; price & "Add to basket" present) |
| Availability | In stock (John Lewis shows "£699.99", "Add to basket", 2-year guarantee) |
| Part number | D8WA6EA#ABU (stated as "Manufacturer part number (MPN) D8WA6EA #ABU" in body) |

**Why it matches exactly:** Page body read at source. "Manufacturer part number (MPN) D8WA6EA #ABU" printed in spec block. Full spec table matches target fields. Price £699.99 shown, "Add to basket" present, 2-year guarantee.

**Conflicts / uncertainty:**
- CPU is Core 7 (i7-class), not Core 5 / i5 — higher tier than target.
- £699.99 is at the upper end of £400–800 but acceptable.
- Price was £899.99 between 04-09 Sep 2026 — current £699.99 is a promo; verify durability.
- Power adapter sold separately (USB-C 65W required).

---

### Candidate 6 — Dell 16 DC16255 (John Lewis, AMD)
| Field | Value |
|---|---|
| Brand | Dell |
| Exact model | Dell 16 DC16255 |
| Manufacturer part number | **C6TH8** |
| CPU | AMD Ryzen 5 7530U (6 cores / 12 threads, up to 4.5GHz) |
| RAM | 16GB LPDDR5X-7500 (onboard) |
| SSD | 512GB PCIe Gen4 NVMe M.2 |
| Screen | 16" 16:10 WUXGA+ (1920x1200) WVA/IPS, 300 nits, anti-glare, non-touch |
| Windows edition | **Windows 11 Home** |
| UK price | N/A (not captured in snippet) |
| Retailer | John Lewis (p115776511) |
| Direct URL | https://www.johnlewis.com/dell-16-dc16255-laptop-amd-ryzen-5-processor-16gb-ram-512gb-ssd-16-full-hd-carbon-black/p115776511 |
| Verification status | **UNVERIFIED** (part number captured in snippet; no price captured; page not directly read) |
| Availability | Unknown |
| Part number | C6TH8 (captured in snippet as "Manufacturer part number (MPN) C6TH8") |

**Why it matches partially:** Snippet contains "Manufacturer part number (MPN) C6TH8", spec set matches target, Windows 11 Home.

**Conflicts / uncertainty:**
- No price captured; no availability captured; page not directly read.
- 16" screen, LPDDR5X onboard — same concerns as Candidate 4.
- No independent retailer cross-reference captured.

---

## Rejected During This Refined Search

| Item | Reason |
|---|---|
| HP 15-fc0049na (John Lewis) | **Unavailable** — "No longer available online", "unlikely to receive more stock" |
| HP 15-fd1010nax (Direct Computers) | £1,140.99 (ex-VAT £950.83) — **outside £400-800**, retailer says "Unavailable" |
| HP 15-fd1010nax (Amazon UK) | Part number D8WB0EA#ABU but price £499.99–£1,140.99 spread; multiple listings show unavailable |
| HP 15-fd1000nax (Core 7) | Core 7 tier — higher than target Core 5/i5 |
| Dell 16 DC16251 | 16" screen, LPDDR5X onboard (soldered), £749 at upper bound |
| Dell 16 DC16255 | No price captured; UNVERIFIED |
| Dell 16 DC16255 (AMD) | No price captured; UNVERIFIED |
| HP 15-fc0049na (John Lewis) | **Unavailable** — "No longer available online" |
| HP 15-fd0001na (Argos) | **No part number captured**; Argos BLOCKED |
| HP 250 G9 (6S6S9EA) | Windows 11 Pro; part number sibling 6S6E8EA exists; refurbished ambiguity |
| Dell Latitude 3540 (29YN0) | Discontinued on Dell UK; OutOfStock on aggregator; price spread 1.3x |
| Dell Inspiron 15 3520 | Discontinued on Dell UK; no part number; Windows 11 Pro variant also exists |
| Dell Inspiron 15 3530 (eSupply) | Windows 11 Pro only; Windows 11 Home not found at this SKU |
| HP 15-fd1010nax | £1,140.99 unavailable; price spread 2.3x; outside £800 |
| HP 15-fd1000nax (Core 7) | Core 7 tier; £699.99 at upper bound |
| All refurbished / Grade A / Grade C / Spanish keyboard / USD-priced | Explicitly excluded by criteria |
| Aggregator-only prices (PriceRunner, compareaprice, e-Catalog) | Not independently verifiable |

---

## Final Candidate Summary

| # | Brand/Model | Part # | CPU | RAM/SSD | Screen | Windows | Price | Retailer(s) | Verified | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HP 15-fd0072na | BM2W6EA | i5-1334U | 16/512 | 15.6" FHD | Home | £459 | Argos | **UNVERIFIED (Argos BLOCKED)** | Candidate |
| 2 | HP 15-fc0049na | BM2U3EA#ABU | Ryzen 5 7530U | 16/512 | 15.6" FHD | Home | N/A | John Lewis | UNVERIFIED | **Unavailable** |
| 3 | Dell Inspiron 3530 | 6CH4H | i5-1334U | 16/512 | 15.6" 120Hz | **Pro** | £524 | eSupply | **VERIFIED** | Candidate (Pro) |
| 4 | Dell 16 DC16251 | 3XGG3 | Core 5 120U | 16/512 | 16" 2K | Home | £749 | John Lewis | **VERIFIED** | Candidate |
| 5 | HP 15-fd1000nax | D8WA6EA#ABU | Core 7 | 16/512 | 15.6" FHD | Home | £699 | John Lewis | **VERIFIED** | Candidate |
| 6 | Dell 16 DC16255 | C6TH8 | Ryzen 5 7530U | 16/512 | 16" WUXGA+ | Home | N/A | John Lewis | **UNVERIFIED** | Candidate |

---

## Production State Confirmation

- HEAD: `39cb525` (unchanged)
- Tracked files: clean
- `data/products.json`: exactly 2 products (ASUS)
- `data/price-history.json`: 15 observations (unchanged)
- `config/products.json`: 2 tracked part numbers (unchanged)
- No commits, no pushes, no production modifications made.

---

## Recommendation

Only **Candidate 3 (Dell Inspiron 3530, 6CH4H)** is fully VERIFIED and available at a mainstream price, but it is Windows 11 **Pro**.

**Candidate 4 (Dell 16 DC16251, 3XGG3)** and **Candidate 5 (HP 15-fd1000nax, D8WA6EA#ABU)** are VERIFIED and Windows 11 Home but have spec deviations (16" screen / LPDDR5X soldered / Core 7 tier / £749-699 price).

**Candidate 1 (HP 15-fd0072na)** has the right spec and price but is on **Argos (BLOCKED)** — cannot be independently verified.

No candidate meets **all** criteria perfectly. Recommend selecting based on which compromises are acceptable, or waiting for better consumer-Home SKUs to appear.