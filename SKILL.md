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