#!/usr/bin/env python3
"""
Get detailed information about a player from multiple APIs.
Aggregates data from Website API, BackOffice API, Wallet API, and Bonus API.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory


def get_player_info(client_id: int, env: str = "qa", 
                    session_token: str = None) -> dict:
    """
    Get comprehensive player information from multiple APIs.
    
    Args:
        client_id: Client ID
        env: Environment (dev, qa, prod)
        session_token: Optional session token for Website API calls
        
    Returns:
        Dictionary with aggregated player information
    """
    print(f"📊 Gathering player information for client {client_id} in {env.upper()}...")
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    player_info = {
        "env": env,
        "client_id": client_id,
        "timestamp": datetime.now().isoformat(),
    }
    
    # 1. BackOffice API - Client details
    print("\n🏢 BackOffice API - Client details...")
    try:
        client_details = clients["backoffice"].get_client_by_id(client_id)
        response_obj = client_details.get("ResponseObject", {})
        
        player_info["backoffice"] = {
            "email": response_obj.get("Email"),
            "userName": response_obj.get("UserName"),
            "firstName": response_obj.get("FirstName"),
            "lastName": response_obj.get("LastName"),
            "phone": response_obj.get("Phone"),
            "country": response_obj.get("CountryId"),
            "currency": response_obj.get("CurrencyId"),
            "state": response_obj.get("State"),
            "isTest": response_obj.get("IsTest"),
            "kycLevel": response_obj.get("KycLevel"),
            "createdAt": response_obj.get("CreatedAt"),
            "lastLogin": response_obj.get("LastLogin"),
        }
        
        print(f"✅ Client details retrieved")
        print(f"   Email: {player_info['backoffice']['email']}")
        print(f"   IsTest: {player_info['backoffice']['isTest']}")
        print(f"   KYC Level: {player_info['backoffice']['kycLevel']}")
        print(f"   State: {player_info['backoffice']['state']}")
        
    except Exception as e:
        print(f"❌ Could not get client details: {e}")
        player_info["backoffice_error"] = str(e)
    
    # 2. Wallet API - Balance
    print("\n💰 Wallet API - Balance...")
    try:
        currency = player_info.get("backoffice", {}).get("currency", "USD")
        balance = clients["wallet"].get_balance(client_id, currency)
        
        player_info["wallet"] = {
            "availableMain": balance.get("AvailableMain", 0),
            "availableBonus": balance.get("AvailableBonus", 0),
            "currency": balance.get("Currency", currency),
            "total": balance.get("AvailableMain", 0) + balance.get("AvailableBonus", 0),
        }
        
        print(f"✅ Balance retrieved")
        print(f"   Available Main: ${player_info['wallet']['availableMain']:.2f}")
        print(f"   Available Bonus: ${player_info['wallet']['availableBonus']:.2f}")
        print(f"   Total: ${player_info['wallet']['total']:.2f} {player_info['wallet']['currency']}")
        
    except Exception as e:
        print(f"❌ Could not get balance: {e}")
        player_info["wallet_error"] = str(e)
    
    # 3. Wallet API - Recent transactions
    print("\n📜 Wallet API - Recent transactions...")
    try:
        transactions = clients["wallet"].get_transactions(client_id, limit=5)
        
        player_info["transactions"] = []
        
        for tx in transactions[:5]:  # Limit to 5
            player_info["transactions"].append({
                "id": tx.get("Id"),
                "type": tx.get("Type"),
                "amount": tx.get("Amount"),
                "currency": tx.get("Currency"),
                "createdAt": tx.get("CreatedAt"),
            })
        
        print(f"✅ Retrieved {len(player_info['transactions'])} recent transactions")
        
    except Exception as e:
        print(f"❌ Could not get transactions: {e}")
        player_info["transactions_error"] = str(e)
    
    # 4. BackOffice API - Client bonuses
    print("\n🎁 BackOffice API - Client bonuses...")
    try:
        bonuses = clients["backoffice"].get_client_bonuses(client_id)
        
        player_info["bonuses"] = {
            "active": [],
            "history": [],
        }
        
        # Process bonuses (structure depends on API response)
        if isinstance(bonuses, list):
            for bonus in bonuses:
                bonus_info = {
                    "id": bonus.get("Id"),
                    "name": bonus.get("Name"),
                    "status": bonus.get("Status"),
                    "amount": bonus.get("Amount"),
                    "currency": bonus.get("CurrencyId"),
                    "createdAt": bonus.get("CreatedAt"),
                }
                
                if bonus.get("Status") == "Active":
                    player_info["bonuses"]["active"].append(bonus_info)
                else:
                    player_info["bonuses"]["history"].append(bonus_info)
        
        print(f"✅ Retrieved bonuses")
        print(f"   Active bonuses: {len(player_info['bonuses']['active'])}")
        print(f"   Bonus history: {len(player_info['bonuses']['history'])}")
        
    except Exception as e:
        print(f"❌ Could not get bonuses: {e}")
        player_info["bonuses_error"] = str(e)
    
    # 5. Website API - Active bonuses (if session token provided)
    if session_token:
        print("\n🌐 Website API - Active bonuses...")
        try:
            clients["website"].set_session_token(session_token)
            active_bonuses = clients["website"].get_active_bonuses()
            
            player_info["website_bonuses"] = active_bonuses
            print(f"✅ Retrieved active bonuses from Website API")
            
        except Exception as e:
            print(f"❌ Could not get website bonuses: {e}")
            player_info["website_bonuses_error"] = str(e)
    
    return player_info


def print_player_summary(player_info: dict):
    """Print formatted player summary."""
    print("\n" + "="*60)
    print("📋 PLAYER SUMMARY")
    print("="*60)
    
    # Basic info
    if player_info.get("backoffice"):
        bo = player_info["backoffice"]
        print(f"\n👤 Basic Info:")
        print(f"   Client ID: {player_info['client_id']}")
        print(f"   Email: {bo.get('email', 'N/A')}")
        print(f"   Username: {bo.get('userName', 'N/A')}")
        print(f"   Name: {bo.get('firstName', '')} {bo.get('lastName', '')}")
        print(f"   Phone: {bo.get('phone', 'N/A')}")
        print(f"   Country ID: {bo.get('country', 'N/A')}")
        print(f"   IsTest: {bo.get('isTest', False)}")
        print(f"   State: {bo.get('state', 'N/A')}")
        print(f"   KYC Level: {bo.get('kycLevel', 'N/A')}")
        print(f"   Created: {bo.get('createdAt', 'N/A')}")
        print(f"   Last Login: {bo.get('lastLogin', 'N/A')}")
    
    # Balance
    if player_info.get("wallet"):
        wallet = player_info["wallet"]
        print(f"\n💰 Balance:")
        print(f"   Available Main: ${wallet['availableMain']:.2f}")
        print(f"   Available Bonus: ${wallet['availableBonus']:.2f}")
        print(f"   Total: ${wallet['total']:.2f} {wallet['currency']}")
    
    # Recent transactions
    if player_info.get("transactions"):
        print(f"\n📜 Recent Transactions:")
        for tx in player_info["transactions"][:3]:
            print(f"   - {tx.get('type', 'N/A')}: ${tx.get('amount', 0):.2f} ({tx.get('createdAt', 'N/A')})")
    
    # Bonuses
    if player_info.get("bonuses"):
        bonuses = player_info["bonuses"]
        print(f"\n🎁 Bonuses:")
        print(f"   Active: {len(bonuses.get('active', []))}")
        print(f"   History: {len(bonuses.get('history', []))}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="Get detailed player information")
    parser.add_argument("client_id", type=int, help="Client ID")
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--token", type=str,
                       help="Session token for Website API calls")
    parser.add_argument("--output", type=str,
                       help="Output file for player info (JSON)")
    parser.add_argument("--quiet", action="store_true",
                       help="Only print summary, no detailed output")
    
    args = parser.parse_args()
    
    try:
        player_info = get_player_info(
            client_id=args.client_id,
            env=args.env,
            session_token=args.token
        )
        
        # Print summary
        if not args.quiet:
            print_player_summary(player_info)
        
        # Save to output file if specified
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w") as f:
                json.dump(player_info, f, indent=2)
            print(f"\n💾 Player info saved to: {output_path}")
        
        # Also save to default location
        default_output = Path(__file__).parent.parent / "last_player_info.json"
        with open(default_output, "w") as f:
            json.dump(player_info, f, indent=2)
        print(f"💾 Also saved to: {default_output}")
        
    except Exception as e:
        print(f"\n❌ Failed to get player info: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()