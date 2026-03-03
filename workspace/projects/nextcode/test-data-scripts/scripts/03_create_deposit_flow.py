#!/usr/bin/env python3
"""
Create deposit flow for a test player via BackOffice API.
Full flow: Create deposit -> Mark as paid -> Verify balance.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory
from generate_test_data import generate_external_transaction_id, save_test_data_log

import requests


def create_deposit_flow(client_id: int, amount: float, env: str = "qa",
                        currency: str = "USD", payment_method_id: int = 104,
                        auto_confirm: bool = False, use_wallet: bool = False) -> dict:
    """
    Execute full deposit flow via BackOffice API.
    
    Args:
        client_id: Client ID
        amount: Deposit amount
        env: Environment (dev, qa, prod)
        currency: Currency code
        payment_method_id: Payment method ID (default: 19 for test)
        auto_confirm: Auto-confirm for prod (safety override)
        
    Returns:
        Dictionary with deposit flow result
    """
    print(f"🏦 Creating deposit flow for client {client_id} in {env.upper()}...")
    print(f"   Amount: ${amount:.2f} {currency}")
    print(f"   Payment Method ID: {payment_method_id}")
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    result = {
        "env": env,
        "client_id": client_id,
        "amount": amount,
        "currency": currency,
        "payment_method_id": payment_method_id,
        "success": False,
    }
    
    # Safety check for prod
    if env == "prod" and clients["config"].get("safety_check") and not auto_confirm:
        # Check if player is marked as test
        try:
            client_info = clients["backoffice"].get_client_by_id(client_id)
            is_test = client_info.get("ResponseObject", {}).get("IsTest", False)
            
            if not is_test:
                print("⚠️  WARNING: Client is NOT marked as test in production!")
                confirm = input("Do you want to proceed? (yes/no): ")
                if confirm.lower() != "yes":
                    print("❌ Operation cancelled")
                    result["cancelled"] = True
                    return result
        except Exception as e:
            print(f"⚠️  Could not verify test status: {e}")
    
    try:
        # Step 1: Ensure player is marked as test
        print("\n🏷️  Step 1: Marking player as test...")
        try:
            clients["backoffice"].change_client_details(
                client_id=client_id,
                updates={"IsTest": True}
            )
            print("✅ Player marked as test")
        except Exception as e:
            print(f"⚠️  Could not mark as test (might be okay): {e}")
        
        # Step 2: Get current balance
        print("\n📊 Step 2: Checking current balance...")
        try:
            balance_before = clients["wallet"].get_balance(client_id, currency)
            result["balance_before"] = balance_before
            print(f"   Balance before: ${balance_before.get('AvailableMain', 0):.2f} {currency}")
        except Exception as e:
            print(f"⚠️  Could not get balance before: {e}")
        
        # Step 3: Create deposit
        print("\n💳 Step 3: Creating deposit...")
        
        if use_wallet:
            # Use Wallet correction (direct balance update)
            print("   Using Wallet correction (direct deposit)...")
            deposit_result = clients["wallet"].create_debit_correction(
                client_id=client_id,
                amount=amount,
                currency=currency,
                reason=f"Test deposit via script - client {client_id}"
            )
            result["deposit_creation"] = deposit_result
            result["deposit_method"] = "wallet_correction"
            print("✅ Wallet correction completed")
            
        else:
            # Use BackOffice deposit flow
            deposit_data = {
                "amount": amount,
                "clientId": client_id,
                "externalTransactionId": generate_external_transaction_id(),
                "partnerPaymentMethodId": payment_method_id,
                "paymentRequestType": "Deposit"
            }
            
            deposit_result = clients["backoffice"].create_manual_payment(deposit_data)
            result["deposit_creation"] = deposit_result
            result["deposit_method"] = "backoffice_deposit"
            
            # Check if deposit was created
            if deposit_result.get("ResponseCode") == "Success":
                print("✅ Deposit created successfully")
                # Some methods return PaymentRequestId, some don't
                payment_request_id = deposit_result.get("ResponseObject", {}).get("Id")
                if payment_request_id:
                    result["payment_request_id"] = payment_request_id
                    print(f"   Payment Request ID = {payment_request_id}")
                else:
                    print("   No Payment Request ID returned (direct deposit)")
            else:
                raise Exception(f"Deposit creation failed: {deposit_result}")
        
        # Step 4: Mark as paid (only for BackOffice deposit with payment_request_id)
        if not use_wallet and result.get("payment_request_id"):
            print(f"\n✅ Step 4: Marking payment {result['payment_request_id']} as paid...")
            try:
                status_result = clients["backoffice"].change_payment_status(
                    payment_request_id=result["payment_request_id"],
                    status="MarkAsPaid",
                    comment=f"Test deposit via script - client {client_id}"
                )
                result["status_change"] = status_result
                print("✅ Payment marked as paid")
            except Exception as e:
                print(f"⚠️  Could not mark as paid (might be okay for direct deposits): {e}")
        else:
            print(f"\n⏭️  Step 4: Skipped ({'Wallet correction used' if use_wallet else 'no payment request ID'})")
        
        # Step 5: Verify new balance
        print("\n📊 Step 5: Verifying new balance...")
        try:
            balance_after = clients["wallet"].get_balance(client_id, currency)
            result["balance_after"] = balance_after
            print(f"   Balance after: ${balance_after.get('AvailableMain', 0):.2f} {currency}")
            
            # Calculate difference
            if result.get("balance_before"):
                diff = balance_after.get('AvailableMain', 0) - result["balance_before"].get('AvailableMain', 0)
                print(f"   Difference: ${diff:.2f}")
                result["balance_difference"] = diff
        except Exception as e:
            print(f"⚠️  Could not verify balance: {e}")
        
        result["success"] = True
        print("\n🎉 Deposit flow completed successfully!")
        
        # Save to test data log
        save_test_data_log({
            "type": "deposit",
            "action": "create_flow",
            **result
        })
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error in deposit flow: {e}")
        result["error"] = str(e)
        raise


def find_payment_method_id(env: str, currency: str, partner_id: int = 5) -> int:
    """
    Find payment method ID for given currency and partner.
    Returns ID or None if not found.
    """
    try:
        # Create API clients to get config
        clients = ApiClientFactory.create_clients(env)
        base_url = clients["config"]["backoffice_api"]
        user_id = clients["config"]["backoffice_user_id"]
        
        # Request payment methods
        url = f"{base_url}/api/PaymentSystem/GetPartnerPaymentMethods"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "UserId": str(user_id)
        }
        filter_data = {"partnerId": partner_id}
        
        response = requests.post(url, json=filter_data, headers=headers)
        response.raise_for_status()
        
        methods = response.json().get("ResponseObject", [])
        
        # Find method with matching currency
        for method in methods:
            if method.get("CurrencyId") == currency and method.get("State") == 1:
                return method.get("Id")
        
        # Fallback to null currency
        for method in methods:
            if method.get("CurrencyId") is None and method.get("State") == 1:
                return method.get("Id")
        
        return None
    except Exception as e:
        print(f"⚠️  Could not find payment method automatically: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Create deposit flow for test player")
    parser.add_argument("client_id", type=int, help="Client ID")
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--amount", type=float, required=True,
                       help="Deposit amount")
    parser.add_argument("--currency", default="USD",
                       help="Currency code (default: USD)")
    parser.add_argument("--payment-method", type=int, default=104,
                       help="Payment method ID (default: 104 for USD/Minebit)")
    parser.add_argument("--auto-find-payment-method", action="store_true",
                       help="Automatically find payment method ID for currency")
    parser.add_argument("--use-wallet", action="store_true",
                       help="Use Wallet correction instead of BackOffice deposit")
    parser.add_argument("--auto-confirm", action="store_true",
                       help="Auto-confirm for prod (bypass safety check)")
    parser.add_argument("--output", type=str,
                       help="Output file for result (JSON)")
    
    args = parser.parse_args()
    
    # Auto-find payment method if requested
    payment_method_id = args.payment_method
    if args.auto_find_payment_method:
        print(f"🔍 Auto-finding payment method for {args.currency}...")
        found_id = find_payment_method_id(args.env, args.currency)
        if found_id:
            payment_method_id = found_id
            print(f"✅ Using payment method ID: {payment_method_id}")
        else:
            print(f"⚠️  Could not find payment method, using default: {payment_method_id}")
    
    try:
        result = create_deposit_flow(
            client_id=args.client_id,
            amount=args.amount,
            env=args.env,
            currency=args.currency,
            payment_method_id=payment_method_id,
            auto_confirm=args.auto_confirm,
            use_wallet=args.use_wallet
        )
        
        print("\n" + "="*50)
        print("📋 DEPOSIT FLOW SUMMARY")
        print("="*50)
        print(f"Client ID: {result['client_id']}")
        print(f"Environment: {result['env'].upper()}")
        print(f"Amount: ${result['amount']:.2f} {result['currency']}")
        print(f"Payment Request ID: {result.get('payment_request_id', 'N/A')}")
        print(f"Success: {result['success']}")
        
        if result.get('balance_before'):
            print(f"Balance Before: ${result['balance_before'].get('AvailableMain', 0):.2f}")
        
        if result.get('balance_after'):
            print(f"Balance After: ${result['balance_after'].get('AvailableMain', 0):.2f}")
        
        if result.get('balance_difference'):
            print(f"Balance Added: ${result['balance_difference']:.2f}")
        
        # Save to output file if specified
        if args.output:
            if args.output == '-':
                # Output JSON to stdout (for Playwright fixture)
                print(json.dumps(result, indent=2))
            else:
                output_path = Path(args.output)
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"\n💾 Result saved to: {output_path}")
        else:
            # Also save to default location if no output specified
            default_output = Path(__file__).parent.parent / "last_deposit_flow.json"
            with open(default_output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"💾 Also saved to: {default_output}")
        
    except Exception as e:
        print(f"\n❌ Deposit flow failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()