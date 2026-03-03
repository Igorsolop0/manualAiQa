#!/usr/bin/env python3
"""
Create a test player for Minebit/NextCode.
Supports creation via GraphQL or Website API, with optional balance setup.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory
from generate_test_data import generate_client_data, save_test_data_log


def create_test_player(env: str = "qa", ticket_id: str = None, 
                       setup_balance: bool = False, balance_amount: float = 100.0,
                       method: str = "graphql") -> dict:
    """
    Create a test player and optionally set up balance.
    
    Args:
        env: Environment (dev, qa, prod)
        ticket_id: Optional Jira ticket ID for email generation
        setup_balance: Whether to set up initial balance
        balance_amount: Amount to add to balance
        method: Registration method (graphql or website)
        
    Returns:
        Dictionary with player data and client information
    """
    print(f"🚀 Creating test player in {env.upper()} environment...")
    
    # Generate client data
    client_data = generate_client_data(ticket_id)
    print(f"📧 Email: {client_data['email']}")
    print(f"🔐 Password: {client_data['password']}")
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    player_info = {
        "env": env,
        "email": client_data["email"],
        "password": client_data["password"],
        "userName": client_data["userName"],
        "registration_method": method,
        "website_api": clients["config"]["website_api"],
        "partner_id": clients["config"]["partner_id"],
    }
    
    try:
        if method.lower() == "graphql":
            # Register via GraphQL
            print("🔄 Registering via GraphQL...")
            graphql_result = clients["graphql"].register_player(
                email=client_data["email"],
                password=client_data["password"],
                partner_id=clients["config"]["partner_id"]
            )
            
            # Extract player data from GraphQL response
            registration_data = graphql_result.get("data", {}).get("playerRegisterUniversal", {})
            player_info["clientId"] = registration_data.get("id")
            player_info["sessionToken"] = registration_data.get("token")
            player_info["state"] = registration_data.get("state")
            
            # Set session token for Website API client
            if player_info["sessionToken"]:
                clients["website"].set_session_token(player_info["sessionToken"])
            
            print(f"✅ GraphQL registration successful!")
            print(f"   Client ID: {player_info.get('clientId')}")
            print(f"   Session token: {player_info.get('sessionToken', '')[:20]}...")
            
        else:
            # Register via Website API
            print("🔄 Registering via Website API...")
            website_result = clients["website"].register_client(client_data)
            
            # Extract player data from Website API response
            response_obj = website_result.get("ResponseObject", {})
            player_info["clientId"] = response_obj.get("Id")
            player_info["sessionToken"] = response_obj.get("Token")
            player_info["state"] = response_obj.get("State")
            
            print(f"✅ Website API registration successful!")
            print(f"   Client ID: {player_info.get('clientId')}")
        
        # Mark player as test in BackOffice
        if player_info.get("clientId"):
            print("🏷️  Marking player as test in BackOffice...")
            try:
                clients["backoffice"].change_client_details(
                    client_id=player_info["clientId"],
                    updates={"IsTest": True}
                )
                print("✅ Player marked as test")
            except Exception as e:
                print(f"⚠️  Could not mark as test (might be okay): {e}")
        
        # Set up balance if requested
        if setup_balance and player_info.get("clientId"):
            print(f"💰 Setting up balance: ${balance_amount}...")
            try:
                # Use Wallet API to add balance (debit correction adds money)
                wallet_result = clients["wallet"].create_debit_correction(
                    client_id=player_info["clientId"],
                    amount=balance_amount,
                    currency=clients["config"]["common"]["default_currency"],
                    reason=f"Test balance setup for player creation"
                )
                
                player_info["balance_setup"] = True
                player_info["balance_amount"] = balance_amount
                player_info["balance_currency"] = clients["config"]["common"]["default_currency"]
                
                print(f"✅ Balance setup successful!")
                
            except Exception as e:
                print(f"❌ Balance setup failed: {e}")
                player_info["balance_setup_error"] = str(e)
        
        # Get actual balance
        if player_info.get("clientId"):
            print("📊 Getting current balance...")
            try:
                balance_result = clients["wallet"].get_balance(
                    client_id=player_info["clientId"],
                    currency=clients["config"]["common"]["default_currency"]
                )
                player_info["actual_balance"] = balance_result
                print(f"💵 Current balance: ${balance_result.get('AvailableMain', 0):.2f}")
            except Exception as e:
                print(f"⚠️  Could not retrieve balance: {e}")
        
        # Save to test data log
        save_test_data_log({
            "type": "player",
            "action": "create",
            **player_info
        })
        
        print(f"\n🎉 Test player creation complete!")
        return player_info
        
    except Exception as e:
        print(f"❌ Error creating test player: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Create a test player for Minebit/NextCode")
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--ticket", type=str, 
                       help="Jira ticket ID (e.g., CT-727) for email generation")
    parser.add_argument("--balance", type=float, default=100.0,
                       help="Initial balance amount (default: 100)")
    parser.add_argument("--no-balance", action="store_true",
                       help="Don't set up initial balance")
    parser.add_argument("--method", choices=["graphql", "website"], default="graphql",
                       help="Registration method (default: graphql)")
    parser.add_argument("--output", type=str,
                       help="Output file for player data (JSON)")
    
    args = parser.parse_args()
    
    try:
        player_info = create_test_player(
            env=args.env,
            ticket_id=args.ticket,
            setup_balance=not args.no_balance,
            balance_amount=args.balance,
            method=args.method
        )
        
        # Print summary
        print("\n" + "="*50)
        print("📋 PLAYER SUMMARY")
        print("="*50)
        print(f"Environment: {player_info['env'].upper()}")
        print(f"Email: {player_info['email']}")
        print(f"Password: {player_info['password']}")
        print(f"Client ID: {player_info.get('clientId', 'N/A')}")
        print(f"User Name: {player_info.get('userName', 'N/A')}")
        print(f"Session Token: {player_info.get('sessionToken', 'N/A')[:30]}...")
        
        if player_info.get('balance_setup'):
            print(f"Initial Balance: ${player_info.get('balance_amount', 0):.2f} {player_info.get('balance_currency', 'USD')}")
        
        if player_info.get('actual_balance'):
            balance = player_info['actual_balance']
            print(f"Current Balance: ${balance.get('AvailableMain', 0):.2f} {balance.get('Currency', 'USD')}")
        
        # Save to output file if specified
        if args.output:
            if args.output == "-":
                # Output JSON to stdout
                print(json.dumps(player_info, indent=2))
            else:
                output_path = Path(args.output)
                with open(output_path, "w") as f:
                    json.dump(player_info, f, indent=2)
                print(f"\n💾 Player data saved to: {output_path}")
        
        # Also save to default location (unless output is stdout)
        if args.output != "-":
            default_output = Path(__file__).parent.parent / "last_player.json"
            with open(default_output, "w") as f:
                json.dump(player_info, f, indent=2)
            print(f"💾 Also saved to: {default_output}")
        
        # Print ready-to-use cURL command for testing
        if player_info.get('sessionToken'):
            print("\n🔧 Quick test command:")
            print(f"curl -H 'Authorization: {player_info['sessionToken']}' \\")
            print(f"  -H 'website-locale: en' \\")
            print(f"  '{player_info['website_api']}/{player_info['partner_id']}/api/v3/Client/GetClientBalance'")
        
    except Exception as e:
        print(f"\n❌ Failed to create test player: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()