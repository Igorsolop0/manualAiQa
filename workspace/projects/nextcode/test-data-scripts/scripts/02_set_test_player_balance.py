#!/usr/bin/env python3
"""
Set balance for an existing test player.
Supports Wallet API corrections and BackOffice deposit flow.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory
from generate_test_data import generate_external_transaction_id, save_test_data_log


def set_player_balance(client_id: int, amount: float, env: str = "qa", 
                       currency: str = "USD", method: str = "wallet") -> dict:
    """
    Set player balance using specified method.
    
    Args:
        client_id: Client ID
        amount: Amount to add
        env: Environment (dev, qa, prod)
        currency: Currency code
        method: Balance method (wallet or backoffice)
        
    Returns:
        Dictionary with operation result
    """
    print(f"💰 Setting balance for client {client_id} in {env.upper()}...")
    print(f"   Amount: ${amount:.2f} {currency}")
    print(f"   Method: {method}")
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    result = {
        "env": env,
        "client_id": client_id,
        "amount": amount,
        "currency": currency,
        "method": method,
        "success": False,
    }
    
    try:
        if method == "wallet":
            # Use Wallet API debit correction (adds money)
            print("🔄 Using Wallet API debit correction...")
            wallet_result = clients["wallet"].create_debit_correction(
                client_id=client_id,
                amount=amount,
                currency=currency,
                reason=f"Test balance setup via script"
            )
            
            result["wallet_result"] = wallet_result
            result["success"] = True
            print("✅ Wallet API balance setup successful!")
            
        elif method == "backoffice":
            # Use BackOffice API to create deposit and mark as paid
            print("🔄 Using BackOffice API deposit flow...")
            
            # First, ensure player is marked as test
            try:
                clients["backoffice"].change_client_details(
                    client_id=client_id,
                    updates={"IsTest": True}
                )
                print("✅ Player marked as test")
            except Exception as e:
                print(f"⚠️  Could not mark as test: {e}")
            
            # Create deposit
            deposit_data = {
                "amount": amount,
                "clientId": client_id,
                "currencyId": currency,
                "externalTransactionId": generate_external_transaction_id(),
                "partnerPaymentMethodId": 19,  # Test payment method
                "paymentRequestType": "Deposit"
            }
            
            print("💳 Creating deposit...")
            deposit_result = clients["backoffice"].create_manual_payment(deposit_data)
            
            payment_request_id = deposit_result.get("ResponseObject", {}).get("Id")
            if not payment_request_id:
                raise Exception(f"Could not get payment request ID from response: {deposit_result}")
            
            result["deposit_creation"] = deposit_result
            result["payment_request_id"] = payment_request_id
            
            # Mark as paid
            print(f"✅ Marking payment {payment_request_id} as paid...")
            status_result = clients["backoffice"].change_payment_status(
                payment_request_id=payment_request_id,
                status="MarkAsPaid",
                comment="Test deposit via script"
            )
            
            result["status_change"] = status_result
            result["success"] = True
            print("✅ BackOffice deposit flow successful!")
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Verify balance
        print("📊 Verifying new balance...")
        try:
            balance_result = clients["wallet"].get_balance(client_id, currency)
            result["verified_balance"] = balance_result
            print(f"💵 Verified balance: ${balance_result.get('AvailableMain', 0):.2f} {balance_result.get('Currency', currency)}")
        except Exception as e:
            print(f"⚠️  Could not verify balance: {e}")
        
        # Save to test data log
        save_test_data_log({
            "type": "balance",
            "action": "set",
            **result
        })
        
        return result
        
    except Exception as e:
        print(f"❌ Error setting balance: {e}")
        result["error"] = str(e)
        raise


def get_player_balance(client_id: int, env: str = "qa", currency: str = "USD") -> dict:
    """
    Get player balance.
    
    Args:
        client_id: Client ID
        env: Environment (dev, qa, prod)
        currency: Currency code
        
    Returns:
        Balance information
    """
    clients = ApiClientFactory.create_clients(env)
    
    try:
        balance = clients["wallet"].get_balance(client_id, currency)
        return balance
    except Exception as e:
        print(f"❌ Error getting balance: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Set balance for a test player")
    parser.add_argument("client_id", type=int, help="Client ID")
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--amount", type=float, required=True,
                       help="Amount to add")
    parser.add_argument("--currency", default="USD",
                       help="Currency code (default: USD)")
    parser.add_argument("--method", choices=["wallet", "backoffice"], default="wallet",
                       help="Method to set balance (default: wallet)")
    parser.add_argument("--check", action="store_true",
                       help="Check current balance without modifying")
    parser.add_argument("--output", type=str,
                       help="Output file for result (JSON)")
    
    args = parser.parse_args()
    
    try:
        if args.check:
            # Just check balance
            print(f"📊 Checking balance for client {args.client_id}...")
            balance = get_player_balance(args.client_id, args.env, args.currency)
            
            print(f"\n💵 Balance for client {args.client_id}:")
            print(f"   Available Main: ${balance.get('AvailableMain', 0):.2f}")
            print(f"   Available Bonus: ${balance.get('AvailableBonus', 0):.2f}")
            print(f"   Currency: {balance.get('Currency', args.currency)}")
            
            if args.output:
                if args.output == "-":
                    # Output JSON to stdout
                    print(json.dumps(balance, indent=2))
                else:
                    with open(args.output, "w") as f:
                        json.dump(balance, f, indent=2)
                    print(f"\n💾 Balance data saved to: {args.output}")
            
        else:
            # Set balance
            result = set_player_balance(
                client_id=args.client_id,
                amount=args.amount,
                env=args.env,
                currency=args.currency,
                method=args.method
            )
            
            print("\n" + "="*50)
            print("📋 BALANCE OPERATION SUMMARY")
            print("="*50)
            print(f"Client ID: {result['client_id']}")
            print(f"Environment: {result['env'].upper()}")
            print(f"Amount: ${result['amount']:.2f} {result['currency']}")
            print(f"Method: {result['method']}")
            print(f"Success: {result['success']}")
            
            if result.get('verified_balance'):
                balance = result['verified_balance']
                print(f"New Balance: ${balance.get('AvailableMain', 0):.2f} {balance.get('Currency', args.currency)}")
            
            # Save to output file if specified
            if args.output:
                if args.output == "-":
                    # Output JSON to stdout
                    print(json.dumps(result, indent=2))
                else:
                    output_path = Path(args.output)
                    with open(output_path, "w") as f:
                        json.dump(result, f, indent=2)
                    print(f"\n💾 Result saved to: {output_path}")
            
            # Also save to default location (unless output is stdout)
            if args.output != "-":
                default_output = Path(__file__).parent.parent / "last_balance_operation.json"
                with open(default_output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"💾 Also saved to: {default_output}")
        
    except Exception as e:
        print(f"\n❌ Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()