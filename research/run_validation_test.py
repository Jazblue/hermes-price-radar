#!/usr/bin/env python3
"""
Test runner for the two ASUS products using the new research validation process.
This script will be run to produce the validation report.
"""

import sys
sys.path.insert(0, "C:/Users/Administrator/hermes-price-radar/research")

from research_validation import run_research_test

if __name__ == "__main__":
    print("=" * 70)
    print("HERMES PRICE RADAR - RESEARCH VALIDATION TEST")
    print("=" * 70)
    print("Testing the new multi-retailer research & validation process")
    print("on the two existing ASUS products.")
    print()
    
    results = run_research_test()
    
    # Generate summary report
    print("=" * 70)
    print("VALIDATION REPORT SUMMARY")
    print("=" * 70)
    
    for product_name, research in results.items():
        print()
        print("PRODUCT: " + product_name)
        print("  Retailers Discovered: " + str(research.retailers_checked_count))
        print("  Retailers Successfully Verified: " + str(research.retailers_verified_count))
        
        if research.lowest_verified_price:
            print("  Lowest Verified Price: " + str(research.lowest_verified_price) + " (" + research.lowest_verified_retailer + ")")
        else:
            print("  Lowest Verified Price: NO VERIFIED PRICES")
        
        for r in research.retailers:
            print("    " + r.retailer + ": " + str(r.price) + " - " + r.validation_status.value + " - " + r.url)
    
    print()
    print("=" * 70)
    print("NOTE: All results are PARTIALLY_VERIFIED because live page")
    print("fetching was not performed in this test environment.")
    print("Full VERIFIED status requires live page fetch and spec confirmation.")
    print("=" * 70)
