#!/usr/bin/env python3
"""
Create a test bonus for Minebit/NextCode via BackOffice API.
Supports various bonus types: welcome, deposit, cashback, freespins.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory
from generate_test_data import generate_bonus_data, save_test_data_log


def create_test_bonus(env: str = "qa", bonus_type: str = "welcome",
                      trigger_type: str = "deposit", client_id: int = None,
                      name: str = None, amount: float = None,
                      turnover_count: int = None, auto_confirm: bool = False) -> dict:
    """
    Create a test bonus campaign via BackOffice API.
    
    Args:
        env: Environment (dev, qa, prod)
        bonus_type: welcome, deposit, cashback, freespins
        trigger_type: deposit, promocode, campaign
        client_id: Optional client ID for targeting
        name: Bonus name (auto-generated if not provided)
        amount: Bonus amount
        turnover_count: Wagering requirement (turnover count)
        auto_confirm: Auto-confirm for prod (safety override)
        
    Returns:
        Dictionary with bonus creation result
    """
    print(f"🎁 Creating test bonus in {env.upper()}...")
    print(f"   Type: {bonus_type}")
    print(f"   Trigger: {trigger_type}")
    if client_id:
        print(f"   Target Client ID: {client_id}")
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    result = {
        "env": env,
        "bonus_type": bonus_type,
        "trigger_type": trigger_type,
        "client_id": client_id,
        "success": False,
    }
    
    # Safety check for prod
    if env == "prod" and clients["config"].get("safety_check") and not auto_confirm:
        confirm = input("⚠️  You are creating a bonus in PRODUCTION. Proceed? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Operation cancelled")
            result["cancelled"] = True
            return result
    
    try:
        # Generate bonus data
        print("\n📝 Generating bonus configuration...")
        bonus_data = generate_bonus_data(bonus_type, trigger_type, client_id)
        
        # Override with provided values
        if name:
            bonus_data["name"] = name
        if amount is not None:
            bonus_data["minAmount"] = amount
            bonus_data["maxAmount"] = amount
        if turnover_count is not None:
            bonus_data["turnoverCount"] = turnover_count
        
        # Add validity period
        now = datetime.now()
        bonus_data["validFrom"] = now.isoformat()
        bonus_data["validTo"] = (now + timedelta(days=30)).isoformat()
        
        # Ensure test flag
        bonus_data["isTest"] = True
        
        result["bonus_data"] = bonus_data
        
        print(f"✅ Bonus configuration:")
        print(f"   Name: {bonus_data['name']}")
        print(f"   Type ID: {bonus_data['bonusTypeId']}")
        print(f"   Turnover: {bonus_data.get('turnoverCount', 'None')}")
        print(f"   Min Amount: {bonus_data.get('minAmount', 0)}")
        print(f"   Max Amount: {bonus_data.get('maxAmount', 0)}")
        
        # Create bonus via BackOffice API
        print("\n🚀 Creating bonus campaign...")
        creation_result = clients["backoffice"].create_bonus_campaign(bonus_data)
        
        result["creation_result"] = creation_result
        
        # Extract bonus ID if available
        if creation_result.get("ResponseObject"):
            bonus_id = creation_result["ResponseObject"].get("Id")
            if bonus_id:
                result["bonus_id"] = bonus_id
                print(f"✅ Bonus created successfully! ID: {bonus_id}")
            else:
                print(f"✅ Bonus created (ID not available in response)")
        else:
            print(f"✅ Bonus creation request sent")
        
        result["success"] = True
        print("\n🎉 Bonus creation completed!")
        
        # Save to test data log
        save_test_data_log({
            "type": "bonus",
            "action": "create",
            **result
        })
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error creating bonus: {e}")
        result["error"] = str(e)
        raise


def list_bonus_templates():
    """Print available bonus templates."""
    print("\n📋 Available Bonus Templates:")
    print("="*60)
    
    templates = {
        "welcome": {
            "description": "Welcome bonus for new players (match bonus)",
            "trigger_options": ["deposit", "promocode"],
            "example": "--type welcome --trigger deposit"
        },
        "deposit": {
            "description": "Deposit bonus (match or percentage)",
            "trigger_options": ["deposit", "promocode", "campaign"],
            "example": "--type deposit --trigger promocode --client-id 12345"
        },
        "cashback": {
            "description": "Weekly/monthly cashback (calculated by Smartico)",
            "trigger_options": ["campaign"],
            "example": "--type cashback --trigger campaign"
        },
        "freespins": {
            "description": "Free spins bonus for specific games",
            "trigger_options": ["deposit", "promocode", "campaign"],
            "example": "--type freespins --trigger promocode"
        }
    }
    
    for bonus_type, info in templates.items():
        print(f"\n🎁 {bonus_type.upper()}")
        print(f"   {info['description']}")
        print(f"   Triggers: {', '.join(info['trigger_options'])}")
        print(f"   Example: {info['example']}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a test bonus for Minebit/NextCode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create welcome bonus
  python 05_create_bonus.py --type welcome --trigger deposit
  
  # Create deposit bonus for specific client
  python 05_create_bonus.py --type deposit --trigger promocode --client-id 123456
  
  # Create cashback bonus
  python 05_create_bonus.py --type cashback --trigger campaign
  
  # List available templates
  python 05_create_bonus.py --list-templates
        """
    )
    
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--type", choices=["welcome", "deposit", "cashback", "freespins"],
                       default="welcome", help="Bonus type (default: welcome)")
    parser.add_argument("--trigger", choices=["deposit", "promocode", "campaign"],
                       default="deposit", help="Trigger type (default: deposit)")
    parser.add_argument("--client-id", type=int,
                       help="Target client ID for bonus")
    parser.add_argument("--name", type=str,
                       help="Bonus name (auto-generated if not provided)")
    parser.add_argument("--amount", type=float,
                       help="Bonus amount")
    parser.add_argument("--turnover", type=int,
                       help="Wagering requirement (turnover count)")
    parser.add_argument("--auto-confirm", action="store_true",
                       help="Auto-confirm for prod (bypass safety check)")
    parser.add_argument("--output", type=str,
                       help="Output file for result (JSON)")
    parser.add_argument("--list-templates", action="store_true",
                       help="List available bonus templates and exit")
    
    args = parser.parse_args()
    
    # List templates if requested
    if args.list_templates:
        list_bonus_templates()
        return
    
    try:
        result = create_test_bonus(
            env=args.env,
            bonus_type=args.type,
            trigger_type=args.trigger,
            client_id=args.client_id,
            name=args.name,
            amount=args.amount,
            turnover_count=args.turnover,
            auto_confirm=args.auto_confirm
        )
        
        print("\n" + "="*50)
        print("📋 BONUS CREATION SUMMARY")
        print("="*50)
        print(f"Environment: {result['env'].upper()}")
        print(f"Bonus Type: {result['bonus_type']}")
        print(f"Trigger: {result['trigger_type']}")
        if result.get('client_id'):
            print(f"Target Client ID: {result['client_id']}")
        if result.get('bonus_id'):
            print(f"Bonus ID: {result['bonus_id']}")
        print(f"Success: {result['success']}")
        
        if result.get('bonus_data'):
            print(f"Name: {result['bonus_data']['name']}")
        
        # Save to output file if specified
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Result saved to: {output_path}")
        
        # Also save to default location
        default_output = Path(__file__).parent.parent / "last_bonus_creation.json"
        with open(default_output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"💾 Also saved to: {default_output}")
        
    except Exception as e:
        print(f"\n❌ Bonus creation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()