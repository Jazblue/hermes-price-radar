#!/usr/bin/env python3
"""
Hermes Price Radar - Playwright Verification for 23 retailer/product pairs.
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
from hermes_tools import web_search
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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

# Retailers to test (domains) - selected as relevant to the price-radar
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
]

def extract_price(content):
    """Extract price from page content using the same patterns as browser_verification.py."""
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
    """Extract availability from page content."""
    content_lower = content.lower()
    if 'out of stock' in content_lower or 'unavailable' in content_lower:
        return 'Out of stock'
    if 'in stock' in content_lower:
        return 'In stock'
    if 'pre-order' in content_lower:
        return 'Pre-order'
    return 'Unknown'

def extract_model(content, expected_model):
    """Extract model number from page content."""
    # Look for the expected model in the content
    if expected_model in content:
        return expected_model
    # Fallback: look for common model patterns
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
    """Get product URL using web_search tool."""
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
    """Test a single product on a single retailer using Playwright."""
    print(f"\\n{'='*70}")
    print(f"Testing: {product['canonical']} @ {retailer_domain}")
    print(f"{'='*70}")
    
    # Step 1: Get product URL via web_search
    print(f"Searching for {product['canonical']} on {retailer_domain}...")
    url, search_error = get_product_url(retailer_domain, product['canonical'])
    if search_error:
        print(f"  Search error: {search_error}")
        return {
            "product": product['canonical'],
            "retailer": retailer_domain,
            "url": None,
            "model_detected": None,
            "price": None,
            "availability": None,
            "verification_status": "UNVERIFIED",
            "failure_reason": f"Search failed: {search_error}",
            "evidence": f"Search error: {search_error}"
        }
    
    if not url:
        print("  No URL found from search")
        return {
            "product": product['canonical'],
            "retailer": retailer_domain,
            "url": None,
            "model_detected": None,
            "price": None,
            "availability": None,
            "verification_status": "UNVERIFIED",
            "failure_reason": "No URL found from search",
            "evidence": "Search returned no URL"
        }
    
    print(f"  Found URL: {url}")
    
    # Step 2: Load page with Playwright
    with sync_playwright() as p:
        # Launch browser with realistic viewport and user agent
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
                page.close()
                context.close()
                browser.close()
                return {
                    "product": product['canonical'],
                    "retailer": retailer_domain,
                    "url": url,
                    "model_detected": None,
                    "price": None,
                    "availability": None,
                    "verification_status": "UNVERIFIED",
                    "failure_reason": f"HTTP {response.status} error",
                    "evidence": f"HTTP {response.status} error"
                }
            
            # Wait for network idle
            page.wait_for_load_state('networkidle', timeout=15000)
            
            # Scroll to trigger lazy loading if needed
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(2000)
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(1000)
            
            # Get page content
            content = page.content()
            final_url = page.url
            
            # Extract information
            price = extract_price(content)
            availability = extract_availability(content)
            model_detected = extract_model(content, product['expected_model'])
            
            # Determine verification status
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
            
            # Prepare evidence
            evidence_parts = []
            if price is not None:
                evidence_parts.append(f"Price: £{price:.2f}")
            else:
                evidence_parts.append("Price: not found")
            evidence_parts.append(f"Availability: {availability}")
            evidence_parts.append(f"Model detected: {model_detected or 'not found'}")
            evidence_parts.append(f"Final URL: {final_url}")
            evidence = " | ".join(evidence_parts)
            
            print(f"  Model: {model_detected}")
            print(f"  Price: £{price:.2f}" if price is not None else "  Price: not found")
            print(f"  Availability: {availability}")
            print(f"  Final URL: {final_url}")
            print(f"  Verification: {verification_status}")
            if failure_reason:
                print(f"  Reason: {failure_reason}")
            print(f"  Evidence: {evidence}")
            
            page.close()
            context.close()
            browser.close()
            
            return {
                "product": product['canonical'],
                "retailer": retailer_domain,
                "url": final_url,
                "model_detected": model_detected,
                "price": price,
                "availability": availability,
                "verification_status": verification_status,
                "failure_reason": failure_reason,
                "evidence": evidence
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
            return {
                "product": product['canonical'],
                "retailer": retailer_domain,
                "url": url,
                "model_detected": None,
                "price": None,
                "availability": None,
                "verification_status": "UNVERIFIED",
                "failure_reason": f"Timeout: {e}",
                "evidence": f"Timeout during page load: {e}"
            }
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
            return {
                "product": product['canonical'],
                "retailer": retailer_domain,
                "url": url,
                "model_detected": None,
                "price": None,
                "availability": None,
                "verification_status": "UNVERIFIED",
                "failure_reason": f"Exception: {e}",
                "evidence": f"Exception during processing: {e}"
            }

def main():
    """Main verification function."""
    print("Hermes Price Radar - Playwright Verification for 23 retailer/product pairs")
    print("=" * 70)
    print(f"Testing {len(PRODUCTS)} products across {len(RETAILERS)} retailers")
    print(f"Total possible combinations: {len(PRODUCTS) * len(RETAILERS)}")
    print("We will test the first 23 combinations.")
    print("=" * 70)
    
    # Build list of 23 (product, retailer) pairs
    test_pairs = []
    for product in PRODUCTS:
        for retailer in RETAILERS:
            if len(test_pairs) >= 23:
                break
            test_pairs.append((product, retailer))
        if len(test_pairs) >= 23:
            break
    
    print(f"Testing {len(test_pairs)} pairs:")
    for i, (product, retailer) in enumerate(test_pairs, 1):
        print(f"  {i}. {product['canonical']} @ {retailer}")
    print()
    
    all_results = []
    
    for i, (product, retailer) in enumerate(test_pairs, 1):
        print(f"\\n{'='*70}")
        print(f"Test {i}/{len(test_pairs)}")
        print(f"{'='*70}")
        result = test_product_on_retailer(product, retailer)
        all_results.append(result)
        # Small delay between requests to be respectful
        if i < len(test_pairs):
            time.sleep(2)
    
    # Summary
    print("\\n" + "=" * 70)
    print("VERIFICATION RESULTS SUMMARY")
    print("=" * 70)
    
    verified_count = 0
    partially_verified_count = 0
    unverified_count = 0
    
    # Group by product
    for product in PRODUCTS:
        product_results = [r for r in all_results if r['product'] == product['canonical']]
        print(f"\\nProduct: {product['canonical']}")
        print("-" * 50)
        
        for r in product_results:
            status = r['verification_status']
            if status == "VERIFIED":
                verified_count += 1
                status_symbol = "✓"
            elif status == "PARTIALLY_VERIFIED":
                partially_verified_count += 1
                status_symbol = "○"
            else:
                unverified_count += 1
                status_symbol = "✗"
            
            print(f"  {status_symbol} {r['retailer']:20} | {status} | Price: {'£{:.2f}'.format(r['price']) if r['price'] else 'N/A':>8} | {r['failure_reason'] or ''}")
    
    print("\\n" + "=" * 70)
    print("OVERALL STATISTICS")
    print("=" * 70)
    print(f"VERIFIED:   {verified_count}")
    print(f"PARTIAL:    {partially_verified_count}")
    print(f"UNVERIFIED: {unverified_count}")
    print(f"TOTAL:      {len(all_results)}")
    
    # Determine overall result
    if verified_count > 0:
        overall_result = "PARTIAL" if verified_count < len(all_results) else "SUCCESS"
    else:
        overall_result = "FAILED"
    
    print(f"\\nOVERALL RESULT: {overall_result}")
    
    # Ensure research directory exists
    import os
    research_dir = '/c/Users/Administrator/hermes-price-radar/research'
    os.makedirs(research_dir, exist_ok=True)
    
    # Save results to file for inspection
    results_file = '/c/Users/Administrator/hermes-price-radar/research/playwright_results_final.json'
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\\nDetailed results saved to: {results_file}")
    
    # Prepare list of retailers tested and prices extracted
    retailers_tested = list(set(r['retailer'] for r in all_results if r['retailer']))
    prices_extracted = [r for r in all_results if r['price'] is not None]
    failure_reasons = {}
    for r in all_results:
        if r['failure_reason']:
            key = r['failure_reason']
            failure_reasons[key] = failure_reasons.get(key, 0) + 1
    
    # Return summary for use in final report
    return {
        "overall_result": overall_result,
        "verified_count": verified_count,
        "partially_verified_count": partially_verified_count,
        "unverified_count": unverified_count,
        "total_tested": len(all_results),
        "retailers_tested": retailers_tested,
        "prices_extracted_count": len(prices_extracted),
        "prices_extracted": [{"product": r['product'], "retailer": r['retailer'], "price": r['price'], "url": r['url']} for r in prices_extracted],
        "failure_reasons": failure_reasons,
        "results": all_results
    }

if __name__ == "__main__":
    main()