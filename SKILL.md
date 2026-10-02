---
name: price-radar
description: "Track UK consumer electronics prices over time with Google Sheets, GitHub, and Telegram alerts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Hermes Price Radar Skill

## Purpose

Track prices of UK consumer electronics products over time, maintain historical data in Google Sheets and GitHub, and send Telegram alerts for meaningful price changes.

## Installation/Location

This skill is located at:
`~/AppData/Local/hermes/profiles/jhermes/skills/price-radar/`

It consists of:
- `SKILL.md` - This documentation file
- The actual skill logic is implemented in the `hermes-price-radar` GitHub repository

## Commands/Examples

* "Search for laptops under £500" - Search for products matching criteria
* "Find me a 16GB laptop under £600" - Specific product search
* "Track this laptop" - Begin tracking a specific product URL
* "Check my tracked products" - Show all currently tracked products
* "Show me products that have dropped in price" - Products with recent price decreases
* "Find the lowest price for this product" - Historical minimum price
* "Update the price radar" - Run a full price check cycle
* "Show me the biggest price drops" - Largest price decreases

## Data Format

### Products Configuration (config/products.json)
Defines what products to track and search parameters.

### Current Products (data/products.json)
Current state of all tracked products with pricing information.

### Price History (data/price-history.json)
Chronological record of all price observations.

### Google Sheets Structure
Three worksheets:
1. **Products** - Current product state
2. **Price History** - All historical observations
3. **Radar** - Human-readable summary

## Price Validation Rules


## Direct Product URL Handling

For every tracked product, the skill must:

* **Capture the direct product URL** from the actual product listing page.
* **Never invent or construct a URL** if the direct URL cannot be verified.
* **Store the URL** in:
  - `data/products.json` (field: `url`)
  - `data/price-history.json` (field: `url`)
  - Google Sheets "Products" worksheet (column: URL)
  - GitHub repository (in the JSON files)
* **Make the URL clickable** in Google Sheets (using the `=HYPERLINK` formula or rich link).
* **Display a clickable "View Product" link** on the Price Radar website.
* **Preserve the source URL** with price-history records so historical observations retain their source.

The skill verifies the URL by extracting it directly from the product page; if no valid URL is found, the product is not tracked.


1. **Accuracy over quantity** - Prefer fewer verified prices over many guesses
2. **No invented prices** - Only record prices clearly indicated as current
3. **Source preservation** - Keep original product URLs when possible
4. **Retailer distinction** - Same model from different retailers = separate observations
5. **Verification required** - Exclude unverifiable prices rather than guessing
6. **Price distinction** - Track current, previous, lowest, and highest recorded prices
7. **Truthful claims** - Only state "lowest price found in this search" if supported

## Google Sheets Integration

Uses Composio MCP to connect to Google Sheets. Creates/updates:

**Products worksheet columns:**
- Product ID, Product, Manufacturer, Model, Category, Retailer, Current Price, Currency, Lowest Recorded, Highest Recorded, Previous Price, Price Change, URL, Availability, Last Checked

**Price History worksheet columns:**
- Timestamp, Product ID, Product, Retailer, Price, Currency, URL, Availability

**Radar worksheet:**
- Human-readable summary of current state

## GitHub Integration

Uses Composio MCP to:
1. Commit updated JSON files (products.json, price-history.json)
2. Push to main branch
3. Update GitHub Pages site (index.html, style.css, app.js, data files)
4. Verify successful push before sending Telegram "website updated" alert

## Telegram Notification Behaviour

Sends alerts ONLY when meaningful changes occur:

- **Significant price decrease** (≥ 5 GBP or ≥ 10% from previous check)
- **New lowest recorded price** for any tracked product
- **Significant price increase** (≥ 5 GBP or ≥ 10% from previous check)
- **Newly discovered tracked product** (first time seeing this product)
- **Important availability change** (in stock → out of stock or vice versa)
- **Successful website update** after a meaningful price change

Message format:
```
PRICE RADAR

[Product Name]
[Retailer]

£[Current Price]

[Change description]
[Additional context if needed]

Website updated.
```

No message sent if no meaningful changes detected.

## Cron Usage

The skill is designed to work with a Hermes cron job:

**Job Name:** `Price Radar Daily Research`
**Schedule:** `0 9 * * *` (09:00 daily UK time)
**Workdir:** `~/hermes-price-radar`

The cron job will:
1. Load tracked product configuration
2. Search for current prices
3. Validate results
4. Compare with stored prices
5. Update Google Sheets
6. Update GitHub repository
7. Update website data
8. Send Telegram only if meaningful changes occurred
9. Record diagnostic information for failures

## How to Add New Product Categories

1. Edit `config/products.json`
2. Add new category object to the `categories` array
3. Specify:
   - `name`: Category identifier (e.g., "phones", "monitors")
   - `search_terms`: Base search query (e.g., "iPhone 15", "4K monitor")
   - `currency`: GBP (currently only GBP supported)
   - `max_price`: Maximum price to consider (in GBP)
   - `retailers`: Array of retailer domains to search
   - `keywords`: Words that must appear in product title
   - `exclude_keywords`: Words that disqualify a product (refurbished, used, etc.)
4. Adjust `global_settings` if needed
5. The skill will automatically process the new category on next run

## How to Troubleshoot Failures

### Skill Not Loading
1. Verify skill directory exists in Hermes skills folder
2. Check Hermes logs for loading errors
3. Ensure SKILL.md is present and valid

### Search Failures
1. Check if Composio search tools are available and configured
2. Verify network connectivity
3. Look for rate limiting or blocking from search sources
4. Confirm search terms return valid results

### Google Sheets Failures
1. Verify Composio MCP is configured for Google Sheets
2. Check OAuth authentication status
3. Confirm spreadsheet "Hermes Price Radar" exists
4. Ensure worksheets have correct column headers
5. Check for quota limits or API restrictions

### GitHub Failures
1. Verify Composio MCP is configured for GitHub
2. Check GitHub authentication (personal access token)
3. Confirm repository `Jazblue/hermes-price-radar` exists and is accessible
4. Ensure write permissions to the repository
5. Check for network or API rate limiting

### Telegram Failures
1. Verify Telegram is configured in Hermes
2. Check bot token and chat ID
3. Confirm message formatting doesn't exceed limits
4. Look for rate limiting from Telegram

### General Diagnostics
1. Check Hermes skill execution logs
2. Review cron job execution history
3. Examine local JSON files for corruption
4. Verify file permissions in workdir
5. Test individual components manually via Hermes CLI

## Known Limitations

1. **Search Dependency**: Currently relies on manual product configuration; automated web search via Composio is planned
2. **Geographic Scope**: UK-focused (GBP prices, UK retailers)
3. **Frequency**: Daily checks only (configurable via cron)
4. **Price Sources**: Depends on configured retailers' websites
5. **JavaScript**: Site functionality requires JavaScript for optimal display

## Future Enhancements

1. **Automated Product Discovery**: Use Composio web search to find products matching criteria
2. **Multiple Currencies**: Support for EUR, USD alongside GBP
3. **Price Prediction**: Basic trend analysis for future price estimation
4. **Advanced Alerts**: Percentage-based thresholds, moving averages
5. **Export Capabilities**: CSV/Excel export of price history
6. **Comparison Views**: Side-by-side product comparisons
7. **Historical Charts**: Visual price trend graphs on website

## Maintenance

- Regularly review `config/products.json` for outdated products
- Monitor Google Sheets for unexpected changes or errors
- Check GitHub commit history for failed updates
- Review Telegram alerts for accuracy and adjust thresholds as needed
- Backup important data periodically despite redundant storage

## Research & Validation Process

The Price Radar uses a rigorous multi-retailer research and validation process:

### DISCOVER -> MATCH -> VERIFY -> RECORD -> COMPARE -> PUBLISH

**NOT:**
SEARCH -> FIND CHEAP NUMBER -> PUBLISH

### 1. Multi-Retailer Search

For every product research run, search multiple UK retailers where the product is realistically available:

- Argos
- Amazon UK
- Currys
- AO
- John Lewis
- Very
- ASUS UK
- Other reputable UK retailers when relevant

### 2. Product Matching

Before recording a price, confirm that the retailer listing is the SAME product:

- Exact model number
- Manufacturer part number where available
- CPU
- RAM
- Storage
- Screen size
- GPU where applicable
- Colour where relevant

Do NOT treat similar-looking laptops as the same product.

### 3. Price Validation

A price must come from the actual retailer product listing whenever possible.

Do NOT treat as verified current prices:
- Search-result snippets
- Old cached prices
- Review pages
- Comparison-site prices
- Marketplace estimates
- Advertised "from" prices

Record:
- Current price
- Availability
- Retailer
- Direct product URL
- Date/time checked
- Product identifier used for matching

### 4. Delivery / Membership Pricing

Clearly distinguish:
- Standard advertised price
- Membership/subscription price
- Voucher/conditional price
- Delivery charges where relevant

Do not present a conditional price as the normal lowest price.

### 5. Price Confidence

Every retailer result has a validation state:

- **VERIFIED** = current product page checked and product/price confirmed
- **PARTIALLY_VERIFIED** = retailer/product identified but price could not be independently confirmed
- **UNVERIFIED** = found through search/discovery only
- **FAILED** = check attempted but failed

Only VERIFIED prices may be used when calculating the lowest verified price.

### 6. Multiple Retailer Results

Internal data model supports multiple retailers per product:

```
Product
  model
  manufacturer
  specifications
  retailers[]
    retailer
    price
    availability
    url
    checked_at
    validation_status
    notes
```

### 7. Lowest Price Calculation

Calculate `lowest_verified_price` ONLY from retailers with `validation_status = VERIFIED`.

Never choose the lowest number simply because it appears in a search result.

### 8. Price History

Maintain historical price records. When a price changes, record:

- Previous price
- New price
- Retailer
- Timestamp
- Product
- Source URL

Do not overwrite historical information unnecessarily.

### 9. Google Sheets

Redesigned to represent multi-retailer research:

**Products worksheet columns:**
Product, Model, Retailer, Price, Availability, Validation Status, Product URL, Checked At, Previous Price, Price Change, Notes

**Summary worksheet columns:**
Product, Lowest Verified Price, Retailer, Number of Retailers Checked, Last Checked, Price Change

### 10. Website

The live website displays:
- Product
- Current lowest verified price
- Retailer offering that price
- Number of retailers checked
- Last checked
- Price history/change where available
- Direct retailer links

Do not display a price as "best price" unless it is based on VERIFIED retailer data.

### 11. Automation

The daily cron/skill follows: DISCOVER -> MATCH -> VERIFY -> RECORD -> COMPARE -> PUBLISH

### 12. Failure Handling

If a retailer cannot be checked, record that fact. Do not invent or estimate a price.

If only one retailer can be verified, explicitly show "1 retailer verified" rather than implying comprehensive market comparison.

### 13. Testing

Use the two existing ASUS products as the test dataset:
- ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue
- ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver

Validation test results:
- PRODUCT 1 (ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue)
  - Retailers discovered: 1 (Argos)
  - Retailers successfully verified: 0
  - Lowest verified price: NO VERIFIED PRICES
  - Argos: £549.0 - PARTIALLY_VERIFIED - https://www.argos.co.uk/product/7741159

- PRODUCT 2 (ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver)
  - Retailers discovered: 1 (Argos)
  - Retailers successfully verified: 0
  - Lowest verified price: NO VERIFIED PRICES
  - Argos: £549.0 - PARTIALLY_VERIFIED - https://www.argos.co.uk/product/7761225

Note: All results are PARTIALLY_VERIFIED because live page fetching was not performed in the test environment. Full VERIFIED status requires live page fetch and spec confirmation.

### 14. Critical Rule

Accuracy is more important than the number of retailers.

If Hermes cannot verify a price, SAY SO.

Never fabricate a retailer price, product match, availability or URL.

DO NOT publish new prices or change the live dataset until the validation report has been reviewed.

