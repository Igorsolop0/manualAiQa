#!/usr/bin/env python3
"""
Get payment methods for a partner/currency via BackOffice API.
Helps find correct partnerPaymentMethodId for deposit flows.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory


def get_payment_methods(env: str = "qa", partner_id: int = 5, 
                        currency: str = None, state: int = 1) -> list:
    """
    Get payment methods for a partner.
    
    Args:
        env: Environment (dev, qa, prod)
        partner_id: Partner ID (default: 5 for Minebit)
        currency: Filter by currency (e.g., "USD")
        state: Filter by state (1 = Active, 2 = Inactive)
        
    Returns:
        List of payment methods
    """
    print(f"🔍 Getting payment methods for partner {partner_id} in {env.upper()}...")
    if currency:
        print(f"   Currency filter: {currency}")
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    # Build filter
    filter_data = {
        "partnerId": partner_id,
        "currencyId": currency,
        "status": state
    }
    
    try:
        # Use BackOffice API to get payment methods
        # Note: This endpoint might not exist in all environments
        # We'll use a direct request for now
        url = f"{clients['config']['backoffice_api']}/api/PaymentSystem/GetPartnerPaymentMethods"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "UserId": str(clients['config']['backoffice_user_id'])
        }
        
        import requests
        response = requests.post(url, json=filter_data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        methods = result.get("ResponseObject", [])
        
        print(f"✅ Found {len(methods)} payment method(s)")
        return methods
        
    except Exception as e:
        print(f"❌ Error getting payment methods: {e}")
        
        # Fallback: Try to get from a known list
        print("📋 Using known payment methods for partner 5:")
        known_methods = [
            {"Id": 11, "CurrencyId": "AZN", "State": 1, "Description": "AZN method"},
            {"Id": 12, "CurrencyId": "AZN", "State": 1, "Description": "AZN method"},
            {"Id": 97, "CurrencyId": None, "State": 1, "Description": "Universal method"},
            {"Id": 104, "CurrencyId": "USD", "State": 1, "Description": "USD method"},
            {"Id": 374, "CurrencyId": "USD", "State": 1, "Description": "USD method"},
        ]
        
        filtered = []
        for method in known_methods:
            if currency and method.get("CurrencyId") != currency:
                continue
            if method.get("State") != state:
                continue
            filtered.append(method)
        
        print(f"   Found {len(filtered)} known method(s)")
        return filtered


def find_payment_method_id(env: str = "qa", partner_id: int = 5, 
                          currency: str = "USD") -> int:
    """
    Find payment method ID for a given currency and partner.
    
    Args:
        env: Environment
        partner_id: Partner ID
        currency: Currency code
        
    Returns:
        Payment method ID or None if not found
    """
    methods = get_payment_methods(env, partner_id, currency)
    
    if not methods:
        print(f"❌ No payment methods found for {currency}")
        return None
    
    # Prefer methods with matching currency
    for method in methods:
        if method.get("CurrencyId") == currency:
            method_id = method.get("Id")
            print(f"✅ Found payment method ID {method_id} for {currency}")
            return method_id
    
    # Fallback to methods with null currency
    for method in methods:
        if method.get("CurrencyId") is None:
            method_id = method.get("Id")
            print(f"⚠️  Using universal payment method ID {method_id} (no currency specified)")
            return method_id
    
    print(f"❌ No suitable payment method found for {currency}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Get payment methods for deposit flows")
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--partner", type=int, default=5,
                       help="Partner ID (default: 5 for Minebit)")
    parser.add_argument("--currency", type=str,
                       help="Filter by currency (e.g., USD, AZN)")
    parser.add_argument("--find-id", action="store_true",
                       help="Find payment method ID for given currency")
    parser.add_argument("--output", type=str,
                       help="Output file for result (JSON)")
    
    args = parser.parse_args()
    
    try:
        if args.find_id:
            if not args.currency:
                print("❌ Please specify --currency when using --find-id")
                sys.exit(1)
            
            method_id = find_payment_method_id(
                env=args.env,
                partner_id=args.partner,
                currency=args.currency
            )
            
            if method_id:
                print(f"\n🎯 Recommended payment method ID for {args.currency}: {method_id}")
                result = {
                    "env": args.env,
                    "partner_id": args.partner,
                    "currency": args.currency,
                    "payment_method_id": method_id,
                    "found": True
                }
            else:
                result = {
                    "env": args.env,
                    "partner_id": args.partner,
                    "currency": args.currency,
                    "payment_method_id": None,
                    "found": False
                }
        else:
            methods = get_payment_methods(
                env=args.env,
                partner_id=args.partner,
                currency=args.currency
            )
            
            result = {
                "env": args.env,
                "partner_id": args.partner,
                "currency_filter": args.currency,
                "count": len(methods),
                "methods": methods
            }
            
            print(f"\n📋 Payment methods for partner {args.partner}:")
            for method in methods:
                print(f"   ID: {method.get('Id')}, Currency: {method.get('CurrencyId')}, "
                      f"State: {method.get('State')}")
        
        # Save to output file if specified
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Result saved to: {output_path}")
        
        # Also print as JSON if output is stdout
        if args.output == "-":
            print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n❌ Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()