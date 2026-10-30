#!/usr/bin/env python3
"""
Test script for one product on one retailer using web_search and Playwright.
"""

import json
import re
import sys
import time
from hermes_tools import web_search
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def extract_price(content):
    patterns = [
        r'Â£(\\d+\\.?\\d*)',
        r'£(\\d+\\.?\\d*)',
        r'fromÂ£(\\d+\\.?\\d*)',
        r'price\":(\\d+\\.?\\d*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    return None

def extract_availability(content):
    content_lower = content.lower()
    if 'out of stock' in content_lower or 'unavailable' in content_lower:
        return 'Out of stock'
    if 'in stock' in content_lower:
        return 'In stock'
    if 'pre-order' in content_lower:
        return 'Pre-order'
    return 'Unknown'

def extract_model(content, expected_model):
    if expected_model in content:
        return expected_model
    model_patterns = [
        r'[Mm]odel[\\s:]*([A-Za-z0-9\\-]+)',
        r'[Pp]art[\\s:]*[Nn]umber[\\s:]*([A-Za-z0-9\\-]+)',
        r'[Ss][Kk][Uu][\\s:]*([A-Za-z0-9\\-]+)',
    ]
    for pattern in model_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def get_product_url(retailer_domain, product_name):
    query = f'"{product_name}" site:{retailer_domain}'
    try:
        result = web_search(query=query, limit=1)
        if result and 'data' in result and 'web' in result['data'] and len(result['data']['web']) > 0:
            url = result['data']['web'][0]['url']
            return url, None
        else:
            return None, "No search results found"
    except Exception as e:
        return None, f"Search exception: {e}"

def test_product_on_retailer(product, retailer_domain):
    print(f"Testing: {product['canonical']} @ {retailer_domain}")
    url, search_error = get_product_url(retailer_domain, product['canonical'])
    if search_error:
        print(f"  Search error: {search_error}")
        return {"status": "search_error", "error": search_error}
    if not url:
        print("  No URL found")
        return {"status": "no_url"}
    print(f"  URL: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        try:
            print(f"  Navigating to: {url}")
            response = page.goto(url, wait_until='networkidle', timeout=45000)
            if response and response.status >= 400:
                print(f"  HTTP Error: {response.status}")
                return {"status": "http_error", "code": response.status}
            page.wait_for_load_state('networkidle', timeout=15000)
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(2000)
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(1000)
            content = page.content()
            final_url = page.url
            price = extract_price(content)
            availability = extract_availability(content)
            model_detected = extract_model(content, product['expected_model'])
            model_match = model_detected and product['expected_model'].lower() in model_detected.lower()
            price_found = price is not None
            if model_match and price_found:
                verification_status = "VERIFIED"
                failure_reason = None
            elif model_match and not price_found:
                verification_status = "PARTIALLY_VERIFIED"
                failure_reason = "Price not found on page"
            elif not model_match:
                verification_status = "UNVERIFIED"
                failure_reason = f"Model mismatch: detected '{model_detected}', expected '{product['expected_model']}'"
            else:
                verification_status = "UNVERIFIED"
                failure_reason = "Could not verify product"
            print(f"  Model: {model_detected}")
            print(f"  Price: £{price:.2f}" if price is not None else "  Price: not found")
            print(f"  Availability: {availability}")
            print(f"  Final URL: {final_url}")
            print(f"  Verification: {verification_status}")
            if failure_reason:
                print(f"  Reason: {failure_reason}")
            page.close()
            context.close()
            browser.close()
            return {
                "status": "ok",
                "product": product['canonical'],
                "retailer": retailer_domain,
                "url": final_url,
                "model_detected": model_detected,
                "price": price,
                "availability": availability,
                "verification_status": verification_status,
                "failure_reason": failure_reason
            }
        except PlaywrightTimeoutError as e:
            print(f"  Timeout error: {e}")
            try:
                page.close()
            except:
                pass
            try:
                context.close()
            except:
                pass
            try:
                browser.close()
            except:
                pass
            return {"status": "timeout", "error": str(e)}
        except Exception as e:
            print(f"  Unexpected error: {e}")
            try:
                page.close()
            except:
                pass
            try:
                context.close()
            except:
                pass
            try:
                browser.close()
            except:
                pass
            return {"status": "exception", "error": str(e)}

if __name__ == "__main__":
    product = {
        "product_id": "asus-vivobook-ai-16in-ryzen5-16gb-512gb-blue-argos",
        "canonical": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
        "model": "M1607KA-MB148W",
        "expected_model": "M1607KA-MB148W",
        "color": "Blue",
    }
    retailer = "argos.co.uk"
    result = test_product_on_retailer(product, retailer)
    print("\\nResult:")
    print(json.dumps(result, indent=2))