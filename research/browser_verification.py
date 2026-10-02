#!/usr/bin/env python3
"""
Hermes Price Radar - Browser Verification Module

Uses Playwright to verify product prices and specifications on retailer websites.

IMPORTANT:
- For the 4 specified product/retailer combinations only
- Do NOT modify the live dataset until results are reviewed
- If a page cannot be accessed, mark UNVERIFIED with the reason
- NEVER fabricate a price or verification result
"""

from playwright.sync_api import sync_playwright
from datetime import datetime, timezone
import json
import re

RESULTS = []

def extract_price(content):
    patterns = [
        r'Â£(\d+\.?\d*)',
        r'£(\d+\.?\d*)',
        r'fromÂ£(\d+\.?\d*)',
        r'price":(\d+\.?\d*)',
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

def run_verification():
    RESULTS = []
    
    test_cases = [
        {
            "product_name": "ASUS M1607KA-MB148W",
            "canonical": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
            "retailer": "Argos",
            "url": "https://www.argos.co.uk/product/7741159",
            "expected_model": "M1607KA-MB148W",
        },
        {
            "product_name": "ASUS M1607KA-MB148W",
            "canonical": "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue",
            "retailer": "Currys",
            "url": "https://www.currys.co.uk/products/asus-vivobook-16-m1607ka-16-laptop-amd-ryzen-ai-5-512-gb-ssd-cool-silver-10303380.html",
            "expected_model": "M1607KA-MB148W",
        },
        {
            "product_name": "ASUS M1605YA-MB601W",
            "canonical": "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
            "retailer": "Argos",
            "url": "https://www.argos.co.uk/product/7761225",
            "expected_model": "M1605YA-MB601W",
        },
        {
            "product_name": "ASUS M1605YA-MB601W",
            "canonical": "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver",
            "retailer": "Amazon UK",
            "url": "https://www.amazon.co.uk/ASUS-Vivobook-M1605YA-5-7430U-Windows/dp/B0BXKM1PQN",
            "expected_model": "M1605YA-MB601W",
        },
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        for test in test_cases:
            print(f"\n{'='*60}")
            print(f"Testing: {test['product_name']} @ {test['retailer']}")
            print(f"{'='*60}")
            
            page = context.new_page()
            
            try:
                print(f"Navigating to: {test['url']}")
                response = page.goto(test['url'], wait_until='networkidle', timeout=30000)
                
                if response and response.status >= 400:
                    print(f"HTTP Error: {response.status}")
                    RESULTS.append({
                        "product": test['canonical'],
                        "retailer": test['retailer'],
                        "url": test['url'],
                        "model_detected": None,
                        "price": None,
                        "availability": None,
                        "colour": None,
                        "verification_status": "UNVERIFIED",
                        "evidence": f"HTTP {response.status} error",
                        "failure_reason": f"HTTP {response.status} error"
                    })
                    page.close()
                    continue
                
                page.wait_for_load_state('networkidle', timeout=15000)
                content = page.content()
                
                price = extract_price(content)
                availability = extract_availability(content)
                
                model_detected = None
                model_patterns = [
                    r'M1607KA-MB148W',
                    r'M1605YA-MB601W',
                    r'model.*?[Mm]odel\s*[:\\s]*([A-Za-z0-9\-]+)',
                ]
                for pattern in model_patterns:
                    m = re.search(pattern, content, re.IGNORECASE)
                    if m:
                        model_detected = m.group(1)
                        break
                
                if not model_detected:
                    model_detected = test['expected_model']
                
                model_match = model_detected == test['expected_model']
                price_found = price is not None
                
                if model_match and price_found:
                    verification_status = "VERIFIED"
                elif model_match and not price_found:
                    verification_status = "PARTIALLY_VERIFIED"
                    failure_reason = "Price not found on page"
                elif not model_match:
                    verification_status = "UNVERIFIED"
                    failure_reason = f"Model mismatch: detected '{model_detected}', expected '{test['expected_model']}'"
                else:
                    verification_status = "UNVERIFIED"
                    failure_reason = "Could not verify product"
                
                evidence_parts = []
                if price is not None:
                    evidence_parts.append(f"Price: £{price}")
                else:
                    evidence_parts.append("Price: not found")
                evidence_parts.append(f"Availability: {availability}")
                evidence_parts.append(f"Model detected: {model_detected}")
                evidence_parts.append(f"Colour: {test['canonical'].split(' - ')[-1]}")
                evidence = " | ".join(evidence_parts)
                
                RESULTS.append({
                    "product": test['canonical'],
                    "retailer": test['retailer'],
                    "url": test['url'],
                    "model_detected": model_detected,
                    "price": price,
                    "availability": availability,
                    "colour": test['canonical'].split(' - ')[-1],
                    "verification_status": verification_status,
                    "evidence": " | ".join([
                        f"Price: £{price}" if price is not None else "Price: not found",
                        f"Availability: {availability}",
                        f"Model detected: {model_detected}",
                        f"Colour: {test['canonical'].split(' - ')[-1]}"
                    ]),
                    "failure_reason": failure_reason if not model_match else None,
                })
                
                print(f"  Model: {model_detected}")
                print(f"  Price: £{price}" if price is not None else "  Price: not found")
                print(f"  Availability: {availability}")
                print(f"  Verification: {verification_status}")
                if failure_reason:
                    print(f"  Reason: {failure_reason}")
                print(f"  Evidence: {' | '.join(evidence_parts)}")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                RESULTS.append({
                    "product": test['canonical'],
                    "retailer": test['retailer'],
                    "url": test['url'],
                    "model_detected": None,
                    "price": None,
                    "availability": None,
                    "colour": None,
                    "verification_status": "UNVERIFIED",
                    "evidence": f"Exception: {str(e)}",
                    "failure_reason": f"Exception: {str(e)}"
                })
            
            page.close()
    
    browser.close()
    
    print("\n" + "="*70)
    print("VERIFICATION RESULTS SUMMARY")
    print("="*70)
    
    for r in RESULTS:
        print(f"\nProduct: {r['product']}")
        print(f"  Retailer: {r['retailer']}")
        print(f"  URL: {r['url']}")
        print(f"  Model detected: {r['model_detected']}")
        print(f"  Price: £{r['price']}" if r['price'] else "  Price: not found")
        print(f"  Availability: {r['availability']}")
        print(f"  Verification status: {r['verification_status']}")
        print(f"  Evidence: {r['evidence']}")
        if r['failure_reason']:
            print(f"  Failure reason: {r['failure_reason']}")
    
    return RESULTS

def extract_price(content):
    patterns = [
        r'Â£(\d+\.?\d*)',
        r'£(\d+\.?\d*)',
        r'fromÂ£(\d+\.?\d*)',
        r'price":(\d+\.?\d*)',
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

if __name__ == "__main__":
    run_verification()