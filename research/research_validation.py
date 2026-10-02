#!/usr/bin/env python3
"""
Hermes Price Radar - Multi-Retailer Research & Validation Module

This module implements the new research & validation process:
DISCOVER -> MATCH -> VERIFY -> RECORD -> COMPARE -> PUBLISH

It does NOT:
SEARCH -> FIND CHEAP NUMBER -> PUBLISH
"""

import json
import re
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum

class ValidationStatus(Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    FAILED = "FAILED"

class PriceType(Enum):
    STANDARD = "STANDARD"
    MEMBERSHIP = "MEMBERSHIP"
    VOUCHER = "VOUCHER"
    CONDITIONAL = "CONDITIONAL"
    FROM_PRICE = "FROM_PRICE"

@dataclass
class RetailerResult:
    """Result from a single retailer for a product"""
    retailer: str
    price: Optional[float]
    availability: Optional[str]
    url: Optional[str]
    checked_at: str
    validation_status: ValidationStatus
    price_type: PriceType
    matched_specs: Dict[str, Any]
    notes: str = ""
    delivery_cost: Optional[float] = None
    membership_required: bool = False

@dataclass
class ProductSpecs:
    """Canonical product specification for matching"""
    manufacturer: str
    model: str
    model_number: Optional[str] = None
    cpu: Optional[str] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    storage_type: Optional[str] = None
    screen_inches: Optional[float] = None
    gpu: Optional[str] = None
    colour: Optional[str] = None
    part_number: Optional[str] = None

@dataclass
class ProductResearch:
    """Complete research result for a product"""
    product_id: str
    canonical_specs: ProductSpecs
    retailers: List[RetailerResult]
    lowest_verified_price: Optional[float] = None
    lowest_verified_retailer: Optional[str] = None
    retailers_verified_count: int = 0
    retailers_checked_count: int = 0
    research_timestamp: str = ""

    def __post_init__(self):
        if not self.research_timestamp:
            self.research_timestamp = datetime.now(timezone.utc).isoformat()
        # Calculate lowest verified price
        verified = [r for r in self.retailers if r.validation_status == ValidationStatus.VERIFIED and r.price is not None]
        self.retailers_verified_count = len(verified)
        self.retailers_checked_count = len(self.retailers)
        if verified:
            lowest = min(verified, key=lambda x: x.price)
            self.lowest_verified_price = lowest.price
            self.lowest_verified_retailer = lowest.retailer

class ProductMatcher:
    """Matches retailer listings to canonical product specs"""
    
    CRITICAL_FIELDS = ["model_number", "cpu", "ram_gb", "storage_gb", "screen_inches"]
    IMPORTANT_FIELDS = ["gpu", "colour", "part_number"]
    
    @classmethod
    def match(cls, listing_specs, canonical):
        """
        Match a retailer listing to canonical product specs.
        Returns: (is_match, matched_fields, mismatched_fields)
        """
        matched = {}
        mismatched = []
        
        # Check critical fields
        for field in cls.CRITICAL_FIELDS:
            canonical_val = getattr(canonical, field)
            listing_val = listing_specs.get(field)
            
            if canonical_val is not None and listing_val is not None:
                if cls._values_match(canonical_val, listing_val):
                    matched[field] = listing_val
                else:
                    mismatched.append(field + ": canonical=" + str(canonical_val) + ", listing=" + str(listing_val))
            elif canonical_val is not None:
                mismatched.append(field + ": missing in listing")
        
        # Check important fields (don't fail match if missing)
        for field in cls.IMPORTANT_FIELDS:
            canonical_val = getattr(canonical, field)
            listing_val = listing_specs.get(field)
            
            if canonical_val is not None and listing_val is not None:
                if cls._values_match(canonical_val, listing_val):
                    matched[field] = listing_val
                else:
                    mismatched.append(field + ": canonical=" + str(canonical_val) + ", listing=" + str(listing_val))
        
        # Match is successful if all critical fields match (or are missing in listing)
        critical_matched = all(
            f not in mismatched for f in cls.CRITICAL_FIELDS
            if getattr(canonical, f) is not None
        )
        
        return critical_matched, matched, mismatched
    
    @staticmethod
    def _values_match(val1, val2):
        """Flexible matching for values"""
        if val1 == val2:
            return True
        # String comparison (case insensitive)
        if isinstance(val1, str) and isinstance(val2, str):
            return val1.lower().strip() == val2.lower().strip()
        # Numeric comparison (allow small differences for GHz)
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if abs(val1 - val2) < 0.1:  # 0.1 GHz tolerance
                return True
        return False

class RetailerResearcher:
    """Base class for retailer-specific research"""
    
    RETAILER_NAME = "BASE"
    
    def search_product(self, specs):
        """Search for a product on this retailer. Override in subclass."""
        raise NotImplementedError
    
    def verify_listing(self, url, specs):
        """Verify a specific product URL. Override in subclass."""
        raise NotImplementedError

# Retailer registry
RETAILER_RESEARCHERS = {}

def register_researcher(researcher_class):
    RETAILER_RESEARCHERS[researcher_class.RETAILER_NAME] = researcher_class
    return researcher_class

# Example retailer implementations would go here
# For the test, we'll create a manual researcher that uses known URLs

class ManualResearcher:
    """Manual researcher for testing - uses known product URLs"""
    
    def __init__(self):
        # Known test URLs for the two ASUS products
        self.test_urls = {
            "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue": {
                "Argos": "https://www.argos.co.uk/product/7741159",
                # Add other retailers when we find them
            },
            "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver": {
                "Argos": "https://www.argos.co.uk/product/7761225",
            }
        }
    
    def research_product(self, product_name, canonical_specs):
        """Research a product across known retailers"""
        retailer_results = []
        
        urls = self.test_urls.get(product_name, {})
        
        for retailer, url in urls.items():
            # In real implementation, this would fetch and parse the page
            # For now, we'll create a PARTIALLY_VERIFIED result since we can't
            # actually fetch the page in this environment
            result = RetailerResult(
                retailer=retailer,
                price=549.0,
                availability="In stock",
                url=url,
                checked_at=datetime.now(timezone.utc).isoformat(),
                validation_status=ValidationStatus.PARTIALLY_VERIFIED,
                price_type=PriceType.STANDARD,
                matched_specs={
                    "model_number": canonical_specs.model_number,
                    "cpu": canonical_specs.cpu,
                    "ram_gb": canonical_specs.ram_gb,
                    "storage_gb": canonical_specs.storage_gb,
                    "screen_inches": canonical_specs.screen_inches
                },
                notes="Manual test - page not actually fetched. Would need live fetch for VERIFIED status."
            )
            retailer_results.append(result)
        
        return ProductResearch(
            product_id=product_name.lower().replace(" ", "-"),
            canonical_specs=canonical_specs,
            retailers=retailer_results
        )

# Canonical specs for the two test products
TEST_PRODUCTS = {
    "ASUS Vivobook AI 16in Ryzen 5 16GB 512GB Laptop - Blue": ProductSpecs(
        manufacturer="ASUS",
        model="Vivobook AI 16in",
        model_number="M1607KA-MB148W",
        cpu="AMD Ryzen AI 5 330",
        ram_gb=16,
        storage_gb=512,
        storage_type="SSD",
        screen_inches=16.0,
        gpu="AMD Radeon",
        colour="Blue",
        part_number="M1607KA-MB148W"
    ),
    "ASUS Vivobook M160 16in R5 16GB 512GB Laptop - Silver": ProductSpecs(
        manufacturer="ASUS",
        model="Vivobook M160",
        model_number="M1605YA-MB601W",
        cpu="AMD Ryzen 5 7430U",
        ram_gb=16,
        storage_gb=512,
        storage_type="SSD",
        screen_inches=16.0,
        gpu="AMD Radeon",
        colour="Silver",
        part_number="M1605YA-MB601W"
    )
}

def run_research_test():
    """Run the research test on the two ASUS products"""
    researcher = ManualResearcher()
    results = {}
    
    for product_name, specs in TEST_PRODUCTS.items():
        print("=" * 60)
        print("Researching: " + product_name)
        print("=" * 60)
        
        research = researcher.research_product(product_name, specs)
        results[product_name] = research
        
        print("Product ID: " + research.product_id)
        print("Canonical Specs:")
        print("  Model: " + specs.model)
        print("  Model Number: " + str(specs.model_number))
        print("  CPU: " + str(specs.cpu))
        print("  RAM: " + str(specs.ram_gb) + "GB")
        print("  Storage: " + str(specs.storage_gb) + "GB " + str(specs.storage_type))
        print("  Screen: " + str(specs.screen_inches) + " inches")
        print("  GPU: " + str(specs.gpu))
        print("  Colour: " + str(specs.colour))
        print("  Part Number: " + str(specs.part_number))
        
        print("")
        print("Retailers Checked: " + str(research.retailers_checked_count))
        print("Retailers Verified: " + str(research.retailers_verified_count))
        if research.lowest_verified_price:
            print("Lowest Verified Price: " + str(research.lowest_verified_price))
        else:
            print("Lowest Verified Price: NO VERIFIED PRICES")
        
        for r in research.retailers:
            print("")
            print("  Retailer: " + r.retailer)
            print("    Price: " + str(r.price))
            print("    Availability: " + str(r.availability))
            print("    URL: " + str(r.url))
            print("    Validation: " + r.validation_status.value)
            print("    Price Type: " + r.price_type.value)
            print("    Matched Specs: " + str(r.matched_specs))
            print("    Notes: " + r.notes)
    
    return results

if __name__ == "__main__":
    run_research_test()
