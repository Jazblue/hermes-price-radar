# Hermes Price Radar

A Hermes skill and project for tracking UK consumer electronics prices over time.

## Features

- Search for products and track prices
- Records price history in Google Sheets
- Maintains a GitHub repository with website
- Sends Telegram alerts for meaningful price changes
- Daily automated price checks via Hermes cron

## Project Structure

```
hermes-price-radar/
├── README.md
├── SKILL.md
├── config/
│   └── products.json
├── data/
│   ├── products.json
│   └── price-history.json
├── docs/
│   └── architecture.md
├── site/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── scripts/
    └── README.md
```

## Installation

1. The Hermes skill is installed automatically when you clone this repository to your Hermes skills directory
2. Configure Google Sheets access via Composio MCP
3. Set up Telegram notifications in Hermes
4. Configure the cron job for daily runs

## Usage

Once installed, you can use the skill with commands like:
- "Search for laptops under £500"
- "Track this laptop"
- "Check my tracked products"
- "Show me products that have dropped in price"

## Configuration

Edit `config/products.json` to add products you want to track.


## Research & Validation Process

The Price Radar implements a rigorous multi-retailer research and validation process:

**DISCOVER -> MATCH -> VERIFY -> RECORD -> COMPARE -> PUBLISH**

### Multi-Retailer Search
Searches multiple UK retailers (Argos, Amazon UK, Currys, AO, John Lewis, Very, ASUS UK, and others) for each product.

### Product Matching
Confirms exact model match using model number, manufacturer part number, CPU, RAM, storage, screen size, GPU, and colour.

### Price Validation
Every price is validated with a confidence level:
- **VERIFIED** - current product page checked and confirmed
- **PARTIALLY_VERIFIED** - retailer/product identified but price not independently confirmed
- **UNVERIFIED** - found through search only
- **FAILED** - check attempted but failed

Only VERIFIED prices are used for lowest price calculations.

### Multi-Retailer Data Model
Supports multiple retailers per product with individual validation status, price type (standard/membership/voucher), availability, and direct URLs.

### Lowest Verified Price
Calculated ONLY from VERIFIED retailer prices. Never from search snippets or estimates.

### Google Sheets Integration
Redesigned worksheets:
- **Products**: Product, Model, Retailer, Price, Availability, Validation Status, Product URL, Checked At, Previous Price, Price Change, Notes
- **Summary**: Product, Lowest Verified Price, Retailer, Number of Retailers Checked, Last Checked, Price Change

### Website
Displays lowest verified price, retailer, number of retailers checked, last checked, price history, and direct retailer links.

### Automation
Daily cron follows: DISCOVER -> MATCH -> VERIFY -> RECORD -> COMPARE -> PUBLISH

### Failure Handling
If a retailer cannot be checked, records the fact. Explicitly shows number of retailers verified vs discovered.

### Validation Test Results
Test run on 2026-10-03, after Argos proved unreadable (HTTP 403 at its Akamai edge).

Canonical identity resolved to exact manufacturer part numbers — marketing titles proved
unreliable, since "M160" matches at least four different ASUS SKUs.

| Part number | Product | Retailers discovered | Verified | Lowest verified price |
|---|---|---|---|---|
| 90NB15F1-M00A60 | Vivobook 16 M1607KA-MB148W (Blue) | 4 | 2 (1 purchasable) | **£549.99** (ASUS UK Store) |
| 90NB10R2-M01820 | Vivobook 16 M1605YA-MB601W (Silver) | 3 | 1 | **£499.99** (ASUS UK Store) |

Notes:
- Laptop Outlet's Blue listing (£619.99) is VERIFIED but **out of stock**, so it is excluded from `lowest_verified`.
- Both Argos listings are **BLOCKED**. Their last known £549.00 is retained as unverified history only, not a current price.
- The Blue product has an **unresolved CPU spec conflict** (Ryzen AI 5 330 vs 340) and is published with that flag visible rather than a guessed value.
- Amazon's "from £398.99" is a marketplace aggregate and is **not** treated as a price.
- AO listings were discovered but could not be page-fetched, so remain UNVERIFIED.

Full evidence: `research/alternative_retailers_20261003.md`, `research/jina_argos_test_20261003.md`,
`research/rejected_matches.md`.

### Data Schema (v2.0)

Canonical product identity is the `manufacturer_part_number`. `config/products.json` holds
discovery config only; `data/products.json` holds canonical tracking state keyed by part
number with nested retailer listings; `data/price-history.json` is an append-only
observation log; `research/` holds discovery evidence and rejected matches.

`lowest_verified` requires VERIFIED + in_stock + standard + non-null price. When nothing
qualifies it is `null` and the site shows "No verified price" — never a fallback number.



## Advanced Search Techniques

For specific hardware requirements (like minimum RAM), you can enhance your product searches by configuring retailer-specific search parameters in `config/products.json`:

### Example: Searching for 16GB+ RAM Laptops
To specifically find laptops with 16GB RAM or more from retailers like Argos that support structured filtering:

```json
{
  "categories": [
    {
      "name": "laptops",
      "search_terms": "laptop",
      "currency": "GBP",
      "max_price": 500,
      "retailers": ["currys.co.uk", "argos.co.uk", "amazon.co.uk", "very.co.uk"],
      "keywords": ["laptop", "notebook"],
      "exclude_keywords": ["refurbished", "used", "second hand"],
      "search_parameters": {
        "ram_gb": "16"  // For Argos: translates to ram-(gb):16/ in URL
      }
    }
  ]
}
```

### Verification Best Practices
Always verify these specifications from actual product listings before considering a product for tracking:

1. **RAM Specification**: Look for explicit "16GB RAM", "8GB RAM", etc. in the product specifications
2. **Current Price**: Ensure the price is clearly marked as current (not "was" or "save" prices)
3. **Exact Model**: Verify the complete model number from product title/details
4. **Retailer**: Confirm the selling matches your configured retailers
5. **Direct URL**: Ensure URLs point to specific product pages, not category/search pages

Do not track products where:
- RAM specification is ambiguous or missing
- Price appears to be a previous/"was" price rather than current
- Model number cannot be definitively identified
- URL does not point to a specific product page

### Argos-Specific Technique
Argos supports structured search parameters in their browsing URLs. For example:
- To find 16GB RAM laptops: Use parameter `ram-(gb):16/` 
- This translates to adding `"search_parameters": {"ram_gb": "16"}` in your category configuration
- The skill will automatically apply these parameters when constructing search queries for supported retailers

## Data Storage

- **Direct Product URLs**: For every tracked product, the skill captures the exact product page URL from the retailer, stores it in JSON files and Google Sheets, and displays a clickable "View Product" link on the website.

- Product configuration: `config/products.json`
- Current product data: `data/products.json`
- Historical price data: `data/price-history.json`
- Google Sheets: "Hermes Price Radar" spreadsheet

## Website

The GitHub Pages site is automatically updated after successful price checks and shows:
- Last updated time
- Number of tracked products
- Current prices
- Lowest/highest recorded prices
- Recent price changes

## Telegram Notifications

You'll receive Telegram alerts only when:
- Significant price decrease occurs
- New lowest recorded price is found
- Significant price increase occurs
- New tracked product is discovered
- Important availability changes
- Website updated after meaningful changes

## Cron Job

A daily cron job runs at 09:00 UK time to:
1. Load tracked product configuration
2. Search for current prices
3. Validate results
4. Update Google Sheets
5. Update GitHub repository
6. Update website data
7. Send Telegram if meaningful changes occurred

## Troubleshooting

Check Hermes logs for detailed error information.
Ensure Composio MCP is properly configured for Google Sheets and GitHub.
Verify Telegram notifications are set up in Hermes.