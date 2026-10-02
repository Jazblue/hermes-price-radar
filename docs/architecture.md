# Hermes Price Radar Architecture

## Overview

The Hermes Price Radar system consists of several interconnected components that work together to track product prices over time.

## Component Diagram

```text
Hermes Cron (09:00 daily)
          ↓
Price Radar Skill (hermes skill)
          ↓
┌───────────────────┐
│ Composio MCP      │
│ - Google Sheets   │
│ - GitHub          │
│ - (Future: Search)│
└───────────────────┘
          ↓
┌───────────────────┐
│ Price Validation  │
│ - Data cleaning   │
│ - Duplicate check │
│ - Price sanity    │
└───────────────────┘
          ↓
┌───────────────────┐
│ Data Storage      │
│ - products.json   │
│ - price-history.json│
│ - Google Sheets   │
└───────────────────┘
          ↓
┌───────────────────┐
│ GitHub Updates    │
│ - Commit data     │
│ - Push to origin  │
│ - Update site     │
└───────────────────┘
          ↓
┌───────────────────┐
│ Telegram Alerts   │
│ - Only on meaningful changes │
└───────────────────┘
```

## Data Flow

### 1. Price Research Phase
- Skill loads product configuration from `config/products.json`
- For each product category, performs web searches (via future search tool or manual configuration)
- Extracts product details: name, manufacturer, model, retailer, price, URL, availability
- Validates extracted data (price sanity checks, URL validation)

### 2. Data Processing Phase
- Compares new prices with existing records in `data/products.json`
- Updates current prices and calculates changes
- Adds new entries to price history in `data/price-history.json`
- Maintains running lowest/highest recorded prices

### 3. Persistence Phase
- Writes updated data to local JSON files:
  - `data/products.json` (current state)
  - `data/price-history.json` (historical observations)
- Updates Google Sheets via Composio MCP:
  - Products tab: current product state
  - Price History tab: new observations
  - Radar tab: human-readable summary

### 4. Distribution Phase
- Commits and pushes data files to GitHub repository
- Updates GitHub Pages site with latest data
- Evaluates if Telegram notification is warranted:
  - Significant price decrease (≥ threshold)
  - New lowest price recorded
  - Significant price increase (≥ threshold)
  - New product discovered
  - Availability changes
  - Website updated after meaningful changes

## Data Models

### Product Configuration (`config/products.json`)
```json
{
  "categories": [
    {
      "name": "laptops",
      "search_terms": "16GB RAM laptop",
      "currency": "GBP",
      "max_price": 600,
      "retailers": ["currys.co.uk", "argos.co.uk", "amazon.co.uk"],
      "keywords": ["laptop", "notebook", "16gb", "ram"],
      "exclude_keywords": ["refurbished", "used"]
    }
  ],
  "global_settings": {
    "price_check_timeout": 30,
    "max_results_per_search": 10,
    "min_price_change_for_alert": 5.0,
    "min_percent_change_for_alert": 10.0
  }
}
```

### Canonical Product (`data/products.json`) — keyed by manufacturer part number
```json
{
  "90NB15F1-M00A60": {
    "product_id": "asus-vivobook-16-m1607ka-mb148w",
    "brand": "ASUS",
    "model": "Vivobook 16 (M1607) Copilot+ PC",
    "manufacturer_part_number": "90NB15F1-M00A60",
    "model_number": "M1607KA-MB148W",
    "marketing_title": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
    "key_specs": { "cpu": "AMD Ryzen AI 5 330", "ram": "16GB DDR5", "storage": "512GB NVMe M.2 SSD" },
    "spec_conflicts": [
      { "field": "cpu", "resolved": false,
        "values": [
          { "value": "AMD Ryzen AI 5 330, 4 Core", "source": "uk.store.asus.com", "source_trust": "manufacturer_uk_store" },
          { "value": "AMD Ryzen AI 5 330, hex core", "source": "argos.co.uk snippet", "source_trust": "retailer_snippet_unverified" }
        ] }
    ],
    "retailers": {
      "asus-uk-store": {
        "retailer": "ASUS UK Store",
        "retailer_product_id": "90NB15F1-M00A60",
        "product_url": "https://uk.store.asus.com/...",
        "price": 549.99,
        "currency": "GBP",
        "price_type": "standard",
        "availability": "in_stock",
        "last_verified": "2026-10-03T00:00:00Z",
        "verification_status": "VERIFIED",
        "verification_method": "direct_page_fetch",
        "verification_source": "https://uk.store.asus.com/...",
        "evidence": "Body read at source: 'Special Price GBP 549.99'",
        "block_reason": null,
        "checked_at": "2026-10-03T00:00:00Z"
      },
      "argos": {
        "retailer": "Argos",
        "retailer_product_id": "7741159",
        "product_url": "https://www.argos.co.uk/product/7741159",
        "price": null,
        "availability": "unknown",
        "verification_status": "BLOCKED",
        "verification_method": "blocked",
        "block_reason": "HTTP 403 at Akamai edge (errors.edgesuite.net)",
        "last_known_price_unverified": 549.0,
        "last_known_price_at": "2026-10-02T14:58:36Z"
      }
    },
    "lowest_verified": {
      "price": 549.99,
      "currency": "GBP",
      "retailer_slug": "asus-uk-store",
      "product_url": "https://uk.store.asus.com/...",
      "retailers_checked": 4,
      "retailers_verified": 2,
      "retailers_verified_and_purchasable": 1,
      "computed_at": "2026-10-03T00:00:00Z"
    }
  }
}
```

### Price History (`data/price-history.json`) — object, not array
```json
{
  "_schema_version": "2.0",
  "observations": [
    {
      "observation_id": "obs_...",
      "observed_at": "2026-10-03T00:00:00Z",
      "manufacturer_part_number": "90NB15F1-M00A60",
      "product_id": "asus-vivobook-16-m1607ka-mb148w",
      "retailer": "ASUS UK Store",
      "retailer_slug": "asus-uk-store",
      "price": 549.99,
      "currency": "GBP",
      "price_type": "standard",
      "availability": "in_stock",
      "verification_status": "VERIFIED",
      "verification_method": "direct_page_fetch",
      "verification_source": "https://uk.store.asus.com/...",
      "product_url": "https://uk.store.asus.com/...",
      "counts_toward_lowest_verified": true
    },
    {
      "observed_at": "2026-10-03T00:00:00Z",
      "retailer": "Argos",
      "price": null,
      "verification_status": "BLOCKED",
      "verification_method": "blocked",
      "block_reason": "HTTP 403 at Akamai edge",
      "counts_toward_lowest_verified": false
    }
  ],
  "migrated_legacy_records": { "records": [] },
  "diagnostics": []
}
```

Rejected near-matches are **not** stored here. They live in `research/rejected_matches.md`
as discovery evidence.

**Frontend contract:** `app.js` reads `payload.observations || payload` and
`payload.products || payload`, so it renders both the v2 object shape and the legacy array
shape. Deploy the frontend and the data together, or the frontend first.


## Research & Validation Process

The Price Radar implements a rigorous multi-retailer research and validation pipeline:

```text
DISCOVER
    |
    v
MATCH (exact model number, part number, CPU, RAM, storage, screen, GPU, colour)
    |
    v
VERIFY (live product page check -> VERIFIED / PARTIALLY_VERIFIED / UNVERIFIED / FAILED)
    |
    v
RECORD (price, availability, URL, validation_status, price_type, delivery_cost, notes)
    |
    v
COMPARE (calculate lowest_verified_price from VERIFIED retailers only)
    |
    v
PUBLISH (update Google Sheets, GitHub, Website, Telegram)
```

### Data Model

**Product** (canonical)
- manufacturer
- model
- model_number
- cpu
- ram_gb
- storage_gb
- storage_type
- screen_inches
- gpu
- colour
- part_number

**RetailerResult** (per retailer per product)
- retailer
- price
- availability
- url
- checked_at
- validation_status (VERIFIED / PARTIALLY_VERIFIED / UNVERIFIED / FAILED)
- price_type (STANDARD / MEMBERSHIP / VOUCHER / CONDITIONAL / FROM_PRICE)
- matched_specs
- notes
- delivery_cost
- membership_required

### Validation States

- **VERIFIED** = live product page checked, exact model match confirmed, current price confirmed
- **PARTIALLY_VERIFIED** = retailer/product identified but price not independently confirmed from live page
- **UNVERIFIED** = found through search/discovery only
- **FAILED** = check attempted but failed

### Lowest Verified Price Calculation

Only retailers with `validation_status = VERIFIED` and `price is not None` are considered.
The minimum price among verified retailers becomes `lowest_verified_price`.

### Google Sheets Schema

**Products Worksheet:**
Product, Model, Retailer, Price, Availability, Validation Status, Product URL, Checked At, Previous Price, Price Change, Notes

**Summary Worksheet:**
Product, Lowest Verified Price, Retailer, Number of Retailers Checked, Last Checked, Price Change

### Automation Flow

The daily cron job executes:
1. DISCOVER - search configured retailers for products matching canonical specs
2. MATCH - confirm exact model match using critical specifications
3. VERIFY - fetch live product page, confirm price and specs
4. RECORD - store price, availability, URL, validation status
5. COMPARE - calculate lowest_verified_price from VERIFIED retailers
6. PUBLISH - update Google Sheets, GitHub data files, website, Telegram

### Failure Handling

- Retailer check failures are recorded, not ignored
- If only 1 retailer verified, explicitly display "1 retailer verified"
- No price estimation or invention ever
- Failed checks do not block other retailers

### Test Validation Results

Run on two ASUS products (Oct 2026):

**ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue**
- Retailers discovered: 1 (Argos)
- Retailers verified: 0
- Lowest verified price: N/A
- Argos: £549.00 - PARTIALLY_VERIFIED

**ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver**
- Retailers discovered: 1 (Argos)
- Retailers verified: 0
- Lowest verified price: N/A
- Argos: £549.00 - PARTIALLY_VERIFIED

Note: Full VERIFIED status requires live page fetching which was not available in test environment.

## Integration Points

### Composio MCP
- **Google Sheets**: Used for persistent storage and backup
- **GitHub**: Used for version control and website publishing
- **Future**: Web search capabilities for product discovery

### Hermes Systems
- **Skill System**: Main logic encapsulated in `price-radar` skill
- **Cron System**: Daily automated execution at 09:00 UK time
- **Telegram**: Notification system for meaningful changes
- **GitHub Pages**: Automatic website deployment from repository

## Security Considerations

- No API keys or secrets stored in repository
- All credentials managed through Hermes configuration and Composio
- Environment variables used for sensitive configuration
- .gitignore prevents accidental commit of sensitive files

## Extensibility

### Adding New Product Categories
1. Add new category object to `config/products.json` categories array
2. Define search terms, price limits, retailers, and keywords
3. The skill will automatically process new categories

### Adding New Data Sources
1. Implement new search/research functions in the skill
2. Add to the product research phase
3. Ensure data validation applies to new sources

### Customizing Alerts
1. Adjust `global_settings` in `config/products.json`
2. Modify notification logic in the skill
3. Adjust thresholds for what constitutes "meaningful" change


### Search Validation & Verification

The Price Radar skill employs rigorous validation to ensure only qualifying products are tracked:

**Pre-Search Validation:**
- Retailer-specific search parameters (e.g., Argos `ram-(gb):16/` for 16GB RAM)
- Keyword inclusion/exclusion filtering
- Price range filtering (min/max)

**Post-Search Verification:**
Before recording any product, the skill verifies:
1. **RAM Specification**: Explicit "16GB RAM" or higher in specifications
2. **Current Price**: Clearly displayed as current (not "was" or discounted)
3. **Model Number**: Complete and unambiguous model identification
4. **Retailer Match**: Confirmed selling retailer
5. **URL Validity**: Direct product page link (not category/search)

Only products passing ALL verification checks are recorded in the system.