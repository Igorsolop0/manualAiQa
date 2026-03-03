#!/usr/bin/env python3
"""
Test Data Orchestrator - Execute sequences of test data setup operations.
Provides predefined scenarios and custom workflow execution.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

# Import other scripts
from importlib.machinery import SourceFileLoader
import os

# Load modules from numbered files
def load_module(name, path):
    loader = SourceFileLoader(name, path)
    return loader.load_module()

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Import from numbered scripts
create_player_module = load_module("create_player", os.path.join(script_dir, "01_create_test_player.py"))
balance_module = load_module("balance", os.path.join(script_dir, "02_set_test_player_balance.py"))
deposit_module = load_module("deposit", os.path.join(script_dir, "03_create_deposit_flow.py"))
info_module = load_module("info", os.path.join(script_dir, "04_get_player_info.py"))
bonus_module = load_module("bonus", os.path.join(script_dir, "05_create_bonus.py"))

# Extract functions
create_test_player = create_player_module.create_test_player
set_player_balance = balance_module.set_player_balance
get_player_balance = balance_module.get_player_balance
create_deposit_flow = deposit_module.create_deposit_flow
get_player_info = info_module.get_player_info
create_test_bonus = bonus_module.create_test_bonus


# Predefined scenarios
SCENARIOS = {
    "player_with_balance": {
        "description": "Create player with initial balance",
        "steps": [
            {"action": "create_player", "setup_balance": True},
        ]
    },
    "player_with_bonus": {
        "description": "Create player with balance and bonus",
        "steps": [
            {"action": "create_player", "setup_balance": True},
            {"action": "create_bonus", "type": "welcome", "trigger": "deposit"},
        ]
    },
    "player_kyc_pending": {
        "description": "Create player with pending KYC status (simulated)",
        "steps": [
            {"action": "create_player", "setup_balance": False},
            {"action": "info", "note": "KYC status needs to be set manually via BackOffice"},
        ]
    },
    "deposit_streak": {
        "description": "Create player with 3+ deposits for streak testing",
        "steps": [
            {"action": "create_player", "setup_balance": False},
            {"action": "deposit", "amount": 20},
            {"action": "deposit", "amount": 30},
            {"action": "deposit", "amount": 50},
        ]
    },
    "high_roller": {
        "description": "Create player with high balance",
        "steps": [
            {"action": "create_player", "setup_balance": True, "balance": 1000},
        ]
    },
    "full_setup": {
        "description": "Complete player setup with balance, deposit history, and bonus",
        "steps": [
            {"action": "create_player", "setup_balance": True, "balance": 100},
            {"action": "deposit", "amount": 30},
            {"action": "create_bonus", "type": "welcome", "trigger": "deposit"},
            {"action": "get_info"},
        ]
    },
}


def execute_scenario(scenario_name: str, env: str = "qa", ticket_id: str = None,
                     output_file: str = None) -> dict:
    """
    Execute a predefined test data scenario.
    
    Args:
        scenario_name: Name of the scenario to execute
        env: Environment (dev, qa, prod)
        ticket_id: Optional Jira ticket ID
        output_file: Optional output file for results
        
    Returns:
        Dictionary with execution results
    """
    if scenario_name not in SCENARIOS:
        print(f"❌ Unknown scenario: {scenario_name}")
        print(f"Available scenarios: {list(SCENARIOS.keys())}")
        return {"error": f"Unknown scenario: {scenario_name}"}
    
    scenario = SCENARIOS[scenario_name]
    
    print("="*60)
    print(f"🎭 Executing Scenario: {scenario_name}")
    print(f"📝 {scenario['description']}")
    print(f"🌍 Environment: {env.upper()}")
    print("="*60)
    
    execution_result = {
        "scenario": scenario_name,
        "env": env,
        "ticket_id": ticket_id,
        "timestamp": datetime.now().isoformat(),
        "steps": [],
        "success": True,
    }
    
    current_player = None
    
    for i, step in enumerate(scenario["steps"], 1):
        print(f"\n📍 Step {i}/{len(scenario['steps'])}: {step['action']}")
        print("-"*40)
        
        step_result = {
            "step": i,
            "action": step["action"],
            "success": False,
        }
        
        try:
            if step["action"] == "create_player":
                # Create player
                player_result = create_test_player(
                    env=env,
                    ticket_id=ticket_id,
                    setup_balance=step.get("setup_balance", False),
                    balance_amount=step.get("balance", 100),
                    method="graphql"
                )
                
                current_player = player_result
                step_result["result"] = player_result
                step_result["success"] = True
                step_result["player_id"] = player_result.get("clientId")
                
            elif step["action"] == "balance":
                # Set balance
                if not current_player or not current_player.get("clientId"):
                    raise Exception("No player created yet")
                
                balance_result = set_player_balance(
                    client_id=current_player["clientId"],
                    amount=step.get("amount", 100),
                    env=env,
                    currency=step.get("currency", "USD"),
                    method=step.get("method", "wallet")
                )
                
                step_result["result"] = balance_result
                step_result["success"] = True
                
            elif step["action"] == "deposit":
                # Create deposit
                if not current_player or not current_player.get("clientId"):
                    raise Exception("No player created yet")
                
                deposit_result = create_deposit_flow(
                    client_id=current_player["clientId"],
                    amount=step.get("amount", 30),
                    env=env
                )
                
                step_result["result"] = deposit_result
                step_result["success"] = True
                
            elif step["action"] == "create_bonus":
                # Create bonus
                bonus_result = create_test_bonus(
                    env=env,
                    bonus_type=step.get("type", "welcome"),
                    trigger_type=step.get("trigger", "deposit"),
                    client_id=current_player.get("clientId") if current_player else None
                )
                
                step_result["result"] = bonus_result
                step_result["success"] = True
                
            elif step["action"] == "get_info":
                # Get player info
                if not current_player or not current_player.get("clientId"):
                    raise Exception("No player created yet")
                
                info_result = get_player_info(
                    client_id=current_player["clientId"],
                    env=env
                )
                
                step_result["result"] = info_result
                step_result["success"] = True
                
            elif step["action"] == "info":
                # Just informational note
                print(f"ℹ️  Note: {step.get('note', 'No note')}")
                step_result["note"] = step.get("note")
                step_result["success"] = True
            
            else:
                print(f"⚠️  Unknown action: {step['action']}")
                step_result["error"] = f"Unknown action: {step['action']}"
        
        except Exception as e:
            print(f"❌ Step failed: {e}")
            step_result["error"] = str(e)
            execution_result["success"] = False
        
        execution_result["steps"].append(step_result)
    
    # Add final player info if available
    if current_player:
        execution_result["player"] = {
            "clientId": current_player.get("clientId"),
            "email": current_player.get("email"),
            "password": current_player.get("password"),
            "sessionToken": current_player.get("sessionToken"),
        }
    
    # Print summary
    print("\n" + "="*60)
    print("📋 EXECUTION SUMMARY")
    print("="*60)
    print(f"Scenario: {scenario_name}")
    print(f"Environment: {env.upper()}")
    print(f"Steps: {len(execution_result['steps'])}")
    print(f"Success: {execution_result['success']}")
    
    if current_player:
        print(f"\n👤 Created Player:")
        print(f"   ID: {current_player.get('clientId')}")
        print(f"   Email: {current_player.get('email')}")
        print(f"   Password: {current_player.get('password')}")
    
    # Save results
    if output_file:
        output_path = Path(output_file)
    else:
        output_path = Path(__file__).parent.parent / f"scenario_{scenario_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_path, "w") as f:
        json.dump(execution_result, f, indent=2, default=str)
    print(f"\n💾 Results saved to: {output_path}")
    
    return execution_result


def list_scenarios():
    """Print available scenarios."""
    print("\n📋 Available Scenarios:")
    print("="*60)
    
    for name, scenario in SCENARIOS.items():
        print(f"\n🎭 {name}")
        print(f"   {scenario['description']}")
        print(f"   Steps: {len(scenario['steps'])}")
        for i, step in enumerate(scenario['steps'], 1):
            print(f"     {i}. {step['action']}")


def main():
    parser = argparse.ArgumentParser(
        description="Test Data Orchestrator - Execute test data setup scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute predefined scenario
  python 07_test_data_orchestrator.py --scenario player_with_balance
  
  # Execute with ticket ID
  python 07_test_data_orchestrator.py --scenario full_setup --ticket CT-727
  
  # List available scenarios
  python 07_test_data_orchestrator.py --list
        """
    )
    
    parser.add_argument("--scenario", type=str,
                       help="Scenario to execute")
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--ticket", type=str,
                       help="Jira ticket ID for email generation")
    parser.add_argument("--output", type=str,
                       help="Output file for results (JSON)")
    parser.add_argument("--list", action="store_true",
                       help="List available scenarios and exit")
    
    args = parser.parse_args()
    
    # List scenarios if requested
    if args.list:
        list_scenarios()
        return
    
    # Require scenario argument
    if not args.scenario:
        parser.print_help()
        print("\n❌ Error: --scenario is required")
        print("Use --list to see available scenarios")
        sys.exit(1)
    
    try:
        result = execute_scenario(
            scenario_name=args.scenario,
            env=args.env,
            ticket_id=args.ticket,
            output_file=args.output
        )
        
        if not result.get("success"):
            sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Scenario execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()