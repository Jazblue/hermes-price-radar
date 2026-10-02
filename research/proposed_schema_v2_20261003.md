# Proposed config/products.json Schema v2 — Part-Number-Keyed Catalog

Date: 2026-10-03
Status: PROPOSAL ONLY — no production file modified.
Evidence base: research/jina_argos_test_20261003.md, research/alternative_retailers_20261003.md

---

## 1. Why the schema changed

The current schema keys products on a retailer marketing title and stores one
retailer/one price per product. The ASUS test run showed three structural failures:

1. **Marketing titles are not identity.** "ASUS Vivobook M160 16in R5 16GB 512GB
   Laptop - Silver" is an Argos-authored string. It does not contain the model number,
   and "M160" matches at least four different ASUS SKUs. Matching on it produced four
   false positives (Ryzen 7/8GB, Ryzen 7/40GB, Ryzen 7 refurb, Ryzen 5 **150**).
2. **One product, many retailers.** Both test products exist at multiple retailers with
   different prices and stock states. A single `retailer` + `current_price` pair per
   product cannot represent that, and forced the out-of-stock Laptop Outlet price to be
   either lost or mistaken for the lowest.
3. **Verification provenance was unrecordable.** `last_checked` cannot express *how* the
   price was obtained. After the Jina run we learned that `https://r.jina.ai/` returns
   HTTP 200 while the body contains `Access Denied`. Any scraper checking status alone
   records a false success. The schema must force the method to be written down.

---

## 2. Identity rule

> **The `manufacturer_part_number` is the primary key. Nothing else identifies a product.**

Rationale: it is assigned by ASUS, is identical across every UK retailer, and is
published in the spec table of retailer pages that are otherwise readable. Marketing
titles are retained as a *display/search aid* only, never as a key.

If a tracked product has no manufacturer part number, it **cannot be tracked** — record
it under `unresolved` and do not publish a price for it.

---

## 3. Field definitions

### Top level

| Field | Type | Notes |
|---|---|---|
| `schema_version` | string | `"2.0"`. Bump on any breaking change. |
| `updated_at` | ISO-8601 | Last write to this file. |
| `discovery` | object | Retains the old categories config (search terms, retailers, price caps). Unchanged in shape. |
| `products` | object | Map: `manufacturer_part_number` → product record. |
| `unresolved` | array | Products discovered but lacking a part number. No prices published. |

### Product record

| Field | Type | Notes |
|---|---|---|
| `product_id` | string | Stable slug, **derived from** the part number. Not authoritative — the map key is. |
| `brand` | string | e.g. `"ASUS"` |
| `model` | string | Manufacturer's model designation, e.g. `"Vivobook 16 (M1607)"` |
| `manufacturer_part_number` | string | **Primary key.** e.g. `"90NB15F1-M00A60"` |
| `model_number` | string\|null | Commercial model, e.g. `"M1607KA-MB148W"`. Used to cross-check the part number. |
| `alternate_part_numbers` | array | Regional/legacy part numbers seen at other retailers. |
| `marketing_title` | string | Retailer-authored title as first seen. Display aid only. |
| `key_specs` | object | `cpu`, `ram`, `storage`, `display`, `gpu`, `os`, `colour`. |
| `spec_conflicts` | array | Contradictions between sources, unresolved. See §6. |
| `retailers` | object | Map: `retailer_slug` → listing record. §4. |
| `lowest_verified` | object\|null | Computed, never hand-entered. §5. |
| `tracking` | object | `enabled`, `added_at`, `notes`. |

### Values

`availability`
: `"in_stock"` · `"out_of_stock"` · `"preorder"` · `"discontinued"` · `"unknown"`

`price_type`
: `"standard"` · `"membership"` · `"voucher"` · `"finance_conditional"`
: Only `standard` may contribute to `lowest_verified`.

`verification_status`
: `"VERIFIED"` · `"PARTIALLY_VERIFIED"` · `"UNVERIFIED"` · `"BLOCKED"` · `"STALE"`
: Only `VERIFIED` may contribute to `lowest_verified`.

`verification_method`
: `"direct_page_fetch"` — page body read at source, content confirmed
: `"structured_data"` — JSON-LD / schema.org parsed from a fetched page
: `"search_snippet"` — only ever seen in search-engine text. **Never publishable.**
: `"aggregator_reported"` — comparison site. Evidence pointer, never a price source.
: `"blocked"` — attempt made, refused. Retains the failure for auditing.

**Mandatory rule:** `"direct_page_fetch"` and `"structured_data"` require a 200 response
**whose body was checked for an error document**. A 200 with `Access Denied` /
`Target URL returned error` in the body must be recorded as `"blocked"`.

---

## 4. Retailer listing record

| Field | Type | Notes |
|---|---|---|
| `retailer` | string | Display name. |
| `retailer_slug` | string | Map key, e.g. `"asus-uk-store"`. |
| `retailer_product_id` | string\|null | Retailer's own SKU/MPN if published. |
| `listing_title` | string | Title as shown on that retailer. |
| `product_url` | string\|null | Direct product URL. **Null when unverified** — never construct one. |
| `price` | number\|null | Numeric GBP. Null when unknown. |
| `currency` | string | `"GBP"` |
| `list_price` | number\|null | Struck-through RRP, for discount display. |
| `price_type` | string | See §3. |
| `availability` | string | See §3. |
| `last_verified` | ISO-8601\|null | When the price was last read at source. |
| `verification_status` | string | See §3. |
| `verification_method` | string | See §3. |
| `verification_source` | string | The exact URL or API endpoint used. |
| `evidence` | string | Verbatim quote of the price/spec text seen. Required when VERIFIED. |
| `block_reason` | string\|null | Populated when `BLOCKED` — e.g. `"HTTP 403 (Akamai edge)"`. |
| `checked_at` | ISO-8601 | When the check ran, successful or not. |

---

## 5. lowest_verified — computation rule

Computed by the skill on each run. A listing qualifies only if **all** hold:

1. `verification_status == "VERIFIED"`
2. `availability == "in_stock"`
3. `price_type == "standard"`
4. `price` is not null

Result is stored as:
```json
"lowest_verified": {
  "price": 499.99,
  "currency": "GBP",
  "retailer_slug": "asus-uk-store",
  "product_url": "https://...",
  "retailers_checked": 2,
  "retailers_verified": 1,
  "computed_at": "2026-10-03T00:00:00Z"
}
```

When **no** listing qualifies, the field is `null` and the website displays
"No verified price". Never fall back to an UNVERIFIED number to avoid an empty state.

---

## 6. spec_conflicts

When two credible sources disagree on a key spec, record both and do not silently pick
one. A conflict on `cpu` or `ram` downgrades the product's match confidence, because it
may mean two different SKUs share a marketing title.

```json
"spec_conflicts": [
  {
    "field": "cpu",
    "values": [
      {"value": "AMD Ryzen AI 5 330 (quad-core)", "source": "uk.store.asus.com"},
      {"value": "AMD Ryzen AI 5 330 (hex-core, 3.1/4.7GHz)", "source": "argos.co.uk snippet"},
      {"value": "AMD Ryzen AI 5 340", "source": "icecat.biz / laptoparena.net"}
    ],
    "resolved": false
  }
]
```

---

## 7. price-history.json record shape (append-only)

```json
{
  "observed_at": "2026-10-03T00:00:00Z",
  "manufacturer_part_number": "90NB15F1-M00A60",
  "product_id": "asus-m1607ka-mb148w",
  "retailer_slug": "asus-uk-store",
  "retailer": "ASUS UK Store",
  "price": 549.99,
  "currency": "GBP",
  "price_type": "standard",
  "availability": "in_stock",
  "verification_status": "VERIFIED",
  "verification_method": "direct_page_fetch",
  "verification_source": "https://uk.store.asus.com/...",
  "product_url": "https://uk.store.asus.com/..."
}
```

Observations are appended for every retailer on every run, including `BLOCKED` and
`UNVERIFIED` ones — so a retailer that was never checkable is visible in the history
rather than silently absent.

---

## 8. Worked example — the two ASUS test products

```json
{
  "schema_version": "2.0",
  "updated_at": "2026-10-03T00:00:00Z",

  "discovery": {
    "categories": [
      {
        "name": "laptops",
        "search_terms": "ASUS Vivobook 16",
        "currency": "GBP",
        "max_price": 700,
        "retailers": [
          "uk.store.asus.com",
          "laptopoutlet.co.uk",
          "argos.co.uk",
          "ao.com",
          "currys.co.uk",
          "johnlewis.com",
          "very.co.uk",
          "amazon.co.uk"
        ],
        "keywords": ["Vivobook"],
        "exclude_keywords": ["refurbished", "used", "renewed"]
      }
    ]
  },

  "products": {
    "90NB15F1-M00A60": {
      "product_id": "asus-vivobook-16-m1607ka-mb148w",
      "brand": "ASUS",
      "model": "Vivobook 16 (M1607) Copilot+ PC",
      "manufacturer_part_number": "90NB15F1-M00A60",
      "model_number": "M1607KA-MB148W",
      "alternate_part_numbers": [],
      "marketing_title": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
      "key_specs": {
        "cpu": "AMD Ryzen AI 5 330",
        "ram": "16GB DDR5",
        "storage": "512GB NVMe M.2 SSD",
        "display": "16in WUXGA IPS 1920x1200",
        "gpu": "AMD Radeon Graphics",
        "os": "Windows 11 Home 64-bit",
        "colour": "Quiet Blue"
      },
      "spec_conflicts": [
        {
          "field": "cpu",
          "values": [
            {"value": "AMD Ryzen AI 5 330, 4 Core-Processor", "source": "uk.store.asus.com"},
            {"value": "AMD Ryzen AI 5 330, hex core, 3.1GHz / 4.7GHz burst", "source": "argos.co.uk search snippet"},
            {"value": "AMD Ryzen AI 5 340", "source": "icecat.biz, laptoparena.net"}
          ],
          "resolved": false
        }
      ],
      "retailers": {
        "asus-uk-store": {
          "retailer": "ASUS UK Store",
          "retailer_slug": "asus-uk-store",
          "retailer_product_id": "90NB15F1-M00A60",
          "listing_title": "ASUS Vivobook 16 (M1607); Copilot+ PC",
          "product_url": "https://uk.store.asus.com/asus-vivobook-16-m1607-copilot-pc-286177081-90nb15f1-m00a60.html",
          "price": 549.99,
          "currency": "GBP",
          "list_price": 749.99,
          "price_type": "standard",
          "availability": "in_stock",
          "last_verified": "2026-10-03T00:00:00Z",
          "verification_status": "VERIFIED",
          "verification_method": "direct_page_fetch",
          "verification_source": "https://uk.store.asus.com/asus-vivobook-16-m1607-copilot-pc-286177081-90nb15f1-m00a60.html",
          "evidence": "Special Price GBP 549.99 / Regular Price GBP 749.99 / You save GBP 200; Model Number: M1607KA-MB148W; Part Number: 90NB15F1-M00A60",
          "block_reason": null,
          "checked_at": "2026-10-03T00:00:00Z"
        },
        "laptopoutlet": {
          "retailer": "Laptop Outlet",
          "retailer_slug": "laptopoutlet",
          "retailer_product_id": "M1607KA-MB148W",
          "listing_title": "ASUS Vivobook 16 M1607KA-MB148W AMD Ryzen AI 5 330 16GB RAM 512GB SSD 16\" Windows 11 Home Copilot+ Laptop",
          "product_url": "https://www.laptopoutlet.co.uk/asus-vivobook-16-90nb15f1-m00a60.html",
          "price": 619.99,
          "currency": "GBP",
          "list_price": 749.99,
          "price_type": "standard",
          "availability": "out_of_stock",
          "last_verified": "2026-10-03T00:00:00Z",
          "verification_status": "VERIFIED",
          "verification_method": "direct_page_fetch",
          "verification_source": "https://www.laptopoutlet.co.uk/asus-vivobook-16-90nb15f1-m00a60.html",
          "evidence": "GBP 619.99 inc. VAT (was GBP 749.99, Save GBP 130); Out of Stock; SKU M1607KA-MB148W; 90NB15F1-M00A60",
          "block_reason": null,
          "checked_at": "2026-10-03T00:00:00Z"
        },
        "argos": {
          "retailer": "Argos",
          "retailer_slug": "argos",
          "retailer_product_id": "7741159",
          "listing_title": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
          "product_url": "https://www.argos.co.uk/product/7741159",
          "price": null,
          "currency": "GBP",
          "list_price": null,
          "price_type": "standard",
          "availability": "unknown",
          "last_verified": null,
          "verification_status": "BLOCKED",
          "verification_method": "blocked",
          "verification_source": "https://r.jina.ai/https://www.argos.co.uk/product/7741159",
          "evidence": "HTTP 200 with body 'Title: Access Denied / Warning: Target URL returned error 403: Forbidden'; direct curl with desktop UA also HTTP 403",
          "block_reason": "HTTP 403 at Akamai edge (errors.edgesuite.net). Confirmed via direct fetch and Jina Reader.",
          "checked_at": "2026-10-03T00:00:00Z"
        },
        "ao": {
          "retailer": "AO",
          "retailer_slug": "ao",
          "retailer_product_id": null,
          "listing_title": "ASUS Vivobook 16 M1607KA-MB148W Copilot+ PC - Blue",
          "product_url": "https://ao.com/product/m1607kamb148w-asus-vivobook-16-m1607kamb148w-laptop--blue-107583-251.aspx",
          "price": null,
          "currency": "GBP",
          "list_price": null,
          "price_type": "standard",
          "availability": "unknown",
          "last_verified": null,
          "verification_status": "UNVERIFIED",
          "verification_method": "search_snippet",
          "verification_source": "web_search (Exa)",
          "evidence": "Model present in URL slug only; page fetch returned CRAWL_UNKNOWN_ERROR",
          "block_reason": null,
          "checked_at": "2026-10-03T00:00:00Z"
        }
      },
      "lowest_verified": {
        "price": 549.99,
        "currency": "GBP",
        "retailer_slug": "asus-uk-store",
        "product_url": "https://uk.store.asus.com/asus-vivobook-16-m1607-copilot-pc-286177081-90nb15f1-m00a60.html",
        "retailers_checked": 4,
        "retailers_verified": 2,
        "computed_at": "2026-10-03T00:00:00Z"
      },
      "tracking": {
        "enabled": true,
        "added_at": "2026-10-02T14:58:36Z",
        "notes": "Argos title maps to M1607KA-MB148W; part number confirmed on ASUS UK store page."
      }
    },

    "90NB10R2-M01820": {
      "product_id": "asus-vivobook-16-m1605ya-mb601w",
      "brand": "ASUS",
      "model": "Vivobook 16 (M1605)",
      "manufacturer_part_number": "90NB10R2-M01820",
      "model_number": "M1605YA-MB601W",
      "alternate_part_numbers": [],
      "marketing_title": "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
      "key_specs": {
        "cpu": "AMD Ryzen 5 7430U",
        "ram": "16GB DDR4",
        "storage": "512GB NVMe M.2 SSD",
        "display": "16in WUXGA IPS 1920x1200",
        "gpu": "AMD Radeon Graphics",
        "os": "Windows 11 Home 64-bit",
        "colour": "Cool Silver"
      },
      "spec_conflicts": [],
      "retailers": {
        "asus-uk-store": {
          "retailer": "ASUS UK Store",
          "retailer_slug": "asus-uk-store",
          "retailer_product_id": "90NB10R2-M01820",
          "listing_title": "ASUS Vivobook 16 (M1605)",
          "product_url": "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
          "price": 499.99,
          "currency": "GBP",
          "list_price": 549.99,
          "price_type": "standard",
          "availability": "in_stock",
          "last_verified": "2026-10-03T00:00:00Z",
          "verification_status": "VERIFIED",
          "verification_method": "direct_page_fetch",
          "verification_source": "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
          "evidence": "Special Price GBP 499.99 / Regular Price GBP 549.99 / Save GBP 50; Model Number: M1605YA-MB601W; Part Number: 90NB10R2-M01820",
          "block_reason": null,
          "checked_at": "2026-10-03T00:00:00Z"
        },
        "argos": {
          "retailer": "Argos",
          "retailer_slug": "argos",
          "retailer_product_id": "7761225",
          "listing_title": "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
          "product_url": "https://www.argos.co.uk/product/7761225",
          "price": null,
          "currency": "GBP",
          "list_price": null,
          "price_type": "standard",
          "availability": "unknown",
          "last_verified": null,
          "verification_status": "BLOCKED",
          "verification_method": "blocked",
          "verification_source": "https://r.jina.ai/https://www.argos.co.uk/product/7761225",
          "evidence": "HTTP 200 with body 'Title: Access Denied / Warning: Target URL returned error 403: Forbidden'; direct curl HTTP 403",
          "block_reason": "HTTP 403 at Akamai edge (errors.edgesuite.net).",
          "checked_at": "2026-10-03T00:00:00Z"
        },
        "amazon": {
          "retailer": "Amazon UK",
          "retailer_slug": "amazon",
          "retailer_product_id": "B0BXKM1PQN",
          "listing_title": "ASUS Vivobook 16 M1605YA Laptop | 16.0\" Full HD Screen | AMD Ryzen 5-7430U | 16GB RAM | 512GB SSD | Windows 11",
          "product_url": "https://www.amazon.co.uk/ASUS-Vivobook-M1605YA-5-7430U-Windows/dp/B0BXKM1PQN",
          "price": null,
          "currency": "GBP",
          "list_price": null,
          "price_type": "standard",
          "availability": "unknown",
          "last_verified": null,
          "verification_status": "UNVERIFIED",
          "verification_method": "aggregator_reported",
          "verification_source": "web_search (Exa)",
          "evidence": "'New & Used (6) from GBP 398.99' - marketplace aggregate, not a current single-seller price. Snippet's own spec table contradicts itself (16GB in title, 8GB in RAM field).",
          "block_reason": null,
          "checked_at": "2026-10-03T00:00:00Z"
        }
      },
      "lowest_verified": {
        "price": 499.99,
        "currency": "GBP",
        "retailer_slug": "asus-uk-store",
        "product_url": "https://uk.store.asus.com/asus-vivobook-16-m1605-224091453-90nb10r2-m01820.html",
        "retailers_checked": 3,
        "retailers_verified": 1,
        "computed_at": "2026-10-03T00:00:00Z"
      },
      "tracking": {
        "enabled": true,
        "added_at": "2026-10-02T14:58:36Z",
        "notes": "Argos page text states 'Model number: M1605YA-MB601W'. Stored Argos price was GBP 549.00; ASUS UK is GBP 499.99 (-49.01) but Argos could not be re-checked, so no change should be recorded yet."
      }
    }
  },

  "unresolved": []
}
```

---

## 9. Rejected candidates — recorded, not tracked

Kept as a `rejected_matches` array per product so the next run does not re-attempt them
and so a future price change on a near-miss cannot silently become a tracked price.

```json
"rejected_matches": [
  {"retailer": "AO", "model": "M1605YA-MB270W", "price": 479, "reason": "Ryzen 7 / 8GB RAM - wrong specification"},
  {"retailer": "Mesh Computers", "model": "M1605YA-MB296W", "price": 699, "reason": "Ryzen 7 7730U / 40GB / 1TB - wrong specification"},
  {"retailer": "Laptop Outlet", "model": "M1605YA-MB456W", "price": null, "reason": "Ryzen 7 7730U / 1TB / refurbished"},
  {"retailer": "Scan", "model": "M1605NAQ-MB077W", "price": null, "reason": "Ryzen 5 150 - different generation; End of Life"}
]
```

---

## 10. What this changes downstream

| Consumer | Change |
|---|---|
| Website | Displays `lowest_verified` or "No verified price". Shows "N of M retailers verified". Renders each verified listing's clickable `product_url`. |
| Google Sheets | Products sheet gains Validation Status, Verification Method, Last Verified columns. Price History appends one row per retailer per run, including BLOCKED rows. |
| Telegram | Alert only fires on a change in a `lowest_verified` price that was `VERIFIED` at both ends of the comparison. An Argos→BLOCKED transition must not fire a "price dropped" alert. |
| Cron | Writes to `price-history.json` unconditionally; recomputes `lowest_verified` after every run. |

---

## 11. Open questions before implementation

1. **Should the Argos listings be kept at all?** They carry the tracked product IDs and
   are the only source for the original £549.00. Keeping them as `BLOCKED` preserves the
   link without publishing a price — recommended. Alternative is retiring them and
   re-keying onto the ASUS UK part numbers.
2. **Does `SPEC_CONFLICT` on the Blue product's CPU block publication?** Same part number
   at two retailers is strong identity evidence, so recommendation is: publish, but
   surface the conflict in the notes. The conflicting third source (Icecat 340) is a
   catalogue aggregator, lower trust than the manufacturer's own store.
3. **`discovery` block retention.** The old `config/products.json` is a category/search
   config; the new catalog is tracking state. Proposing they live in one file, split into
   `discovery` and `products`. Alternative is two files. This is a structural choice
   worth settling before anything is written.