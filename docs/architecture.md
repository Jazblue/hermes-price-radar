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

### Current Products (`data/products.json`)
```json
{
  "product-id-1": {
    "product_id": "product-id-1",
    "product": "Lenovo IdeaPad 5 15ABR8",
    "manufacturer": "Lenovo",
    "model": "82SV000BUK",
    "category": "laptops",
    "retailer": "Currys",
    "current_price": 499.99,
    "currency": "GBP",
    "lowest_recorded": 479.99,
    "highest_recorded": 529.99,
    "previous_price": 519.99,
    "price_change": -20.00,
    "url": "https://www.currys.co.uk/...",
    "availability": "In stock",
    "last_checked": "2026-10-05T09:00:00Z"
  }
}
```

### Price History (`data/price-history.json`)
```json
[
  {
    "timestamp": "2026-10-03T09:00:00Z",
    "product_id": "product-id-1",
    "product": "Lenovo IdeaPad 5 15ABR8",
    "retailer": "Currys",
    "price": 519.99,
    "currency": "GBP",
    "url": "https://www.currys.co.uk/...",
    "availability": "In stock"
  },
  {
    "timestamp": "2026-10-04T09:00:00Z",
    "product_id": "product-id-1",
    "product": "Lenovo IdeaPad 5 15ABR8",
    "retailer": "Currys",
    "price": 499.99,
    "currency": "GBP",
    "url": "https://www.currys.co.uk/...",
    "availability": "In stock"
  }
]
```

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