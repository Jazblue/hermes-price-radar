#!/usr/bin/env python3
"""
Hermes Price Radar - Playwright Verification Experiment
Tests Playwright retrieval of current laptop prices from retailer product pages.

IMPORTANT:
- Do NOT modify data/products.json or data/price-history.json
- Do NOT publish or commit any unverified prices
- If a page cannot be accessed or price cannot be reliably extracted, mark accordingly
- NEVER fabricate a price or verification result
"""

import json
import re
import sys
import time
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Retailers to test (domains)
RETAILERS = [
    "argos.co.uk",
    "amazon.co.uk",
    "currys.co.uk",
    "ao.com",
    "johnlewis.com",
    "very.co.uk",
    "asus.com",
    "ebuyer.com",
    "scan.co.uk",
    "pcworld.co.uk",
    "microless.co.uk",
    "teknoz.com",
    "laptopsdirect.co.uk",
    "misco.co.uk",
    "currys.co.uk",  # duplicate for variety? we'll make unique later
]

# Products to test (from existing tracked products)
PRODUCTS = [
    {
        "product_id": "asus-vivobook-ai-16in-ryzen5-16gb-512gb-blue-argos",
        "canonical": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
        "model": "M1607KA-MB148W",
        "expected_model": "M1607KA-MB148W",
        "color": "Blue",
    },
    {
        "product_id": "asus-vivobook-m160-16in-r5-16gb-512gb-silver-argos",
        "canonical": "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
        "model": "M1605YA-MB601W",
        "expected_model": "M1605YA-MB601W",
        "color": "Silver",
    },
]

def extract_price_from_content(content):
    """Extract price from page content using multiple strategies."""
    # Strategy 1: Look for JSON-LD offers
    json_ld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    json_ld_matches = re.findall(json_ld_pattern, content, re.IGNORECASE | re.DOTALL)
    for json_str in json_ld_matches:
        try:
            data = json.loads(json_str)
            # Handle @graph or single object
            if isinstance(data, dict) and data.get('@type') == 'Offer':
                price = data.get('price')
                if price:
                    return float(price)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'Offer':
                        price = item.get('price')
                        if price:
                            return float(price)
        except (json.JSONDecodeError, ValueError, TypeError):
            continue
    
    # Strategy 2: Look for price in meta tags
    meta_pattern = r'<meta[^>]*itemprop=["\']price["\'][^>]*content=["\']([^"\']*)["\']'
    meta_match = re.search(meta_pattern, content, re.IGNORECASE)
    if meta_match:
        try:
            return float(meta_match.group(1))
        except ValueError:
            pass
    
    # Strategy 3: Look for common price patterns in visible text
    # GBP patterns
    patterns = [
        r'£\s*(\d+[,.]?\d*)',
        r'&#163;\s*(\d+[,.]?\d*)',
        r'&pound;\s*(\d+[,.]?\d*)',
        r'GBP\s*(\d+[,.]?\d*)',
        r'price\D*(\d+[,.]?\d*)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # Clean the match
            cleaned = match.replace(',', '.')
            try:
                price = float(cleaned)
                # Reasonable price range for laptops: £100 - £5000
                if 100 <= price <= 5000:
                    return price
            except ValueError:
                continue
    
    return None

def extract_availability_from_content(content):
    """Extract availability from page content."""
    content_lower = content.lower()
    if 'out of stock' in content_lower or 'unavailable' in content_lower or 'not available' in content_lower:
        return 'Out of stock'
    if 'in stock' in content_lower or 'available' in content_lower or 'add to basket' in content_lower or 'add to cart' in content_lower:
        return 'In stock'
    if 'pre-order' in content_lower or 'preorder' in content_lower:
        return 'Pre-order'
    return 'Unknown'

def extract_model_from_content(content, expected_model):
    """Extract model number from page content."""
    # Look for JSON-LD model
    json_ld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    json_ld_matches = re.findall(json_ld_pattern, content, re.IGNORECASE | re.DOTALL)
    for json_str in json_ld_matches:
        try:
            data = json.loads(json_str)
            if isinstance(data, dict):
                model = data.get('model') or data.get('productID') or data.get('sku')
                if model and isinstance(model, str):
                    return model.strip()
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        model = item.get('model') or item.get('productID') or item.get('sku')
                        if model and isinstance(model, str):
                            return model.strip()
        except (json.JSONDecodeError, TypeError):
            continue
    
    # Look for model in meta tags
    meta_pattern = r'<meta[^>]*itemprop=["\']model["\'][^>]*content=["\']([^"\']*)["\']'
    meta_match = re.search(meta_pattern, content, re.IGNORECASE)
    if meta_match:
        return meta_match.group(1).strip()
    
    # Look for model in text (specific patterns)
    model_patterns = [
        rf'{expected_model}[\s\-]',
        rf'model[\s:]*[{expected_model[0]}][A-Za-z0-9\-]+',
        r'[Mm]odel[\s:]*([A-Za-z0-9\-]+)',
        r'[Pp]art[\s:]*[Nn]umber[\s:]*([A-Za-z0-9\-]+)',
        r'[Ss][Kk][Uu][\s:]*([A-Za-z0-9\-]+)',
    ]
    for pattern in model_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            if match.lastindex:
                return match.group(1).strip()
            else:
                return match.group(0).strip()
    
    return None

def search_product_url(retailer_domain, product_name):
    """Search for product URL using Exa via agent-reach (mcporter)."""
    import subprocess
    query = f'"{product_name}" site:{retailer_domain}'
    cmd = ['mcporter', 'call', 'exa.web_search_exa', f'query={query}', 'numResults=1']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None, f"Search failed: {result.stderr}"
        output = result.stdout.strip()
        # Extract URL from output
        lines = output.split('\n')
        for line in lines:
            if line.startswith('URL:'):
                url = line.split('URL:', 1)[1].strip()
                return url, None
        # If not found, maybe the first line contains URL?
        if output.startswith('http'):
            return output.split()[0], None
        return None, f"Could not parse URL from output: {output[:200]}"
    except subprocess.TimeoutExpired:
        return None, "Search timeout"
    except Exception as e:
        return None, f"Search exception: {e}"

def test_product_on_retailer(product, retailer_domain):
    """Test a single product on a single retailer using Playwright."""
    print(f"\n{'=
