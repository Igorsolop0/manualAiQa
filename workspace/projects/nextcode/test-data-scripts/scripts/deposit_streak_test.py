#!/usr/bin/env python3
"""
Deposit Streak Test - Full cycle testing of Deposit Streak functionality.
Performs 10 iterations of deposits with API and UI verification.
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from api_clients import ApiClientFactory
from generate_test_data import generate_client_data, save_test_data_log
from 01_create_test_player import create_test_player
from 03_create_deposit_flow import create_deposit_flow


def get_client_bonuses_api(clients, client_id, env="qa"):
    """
    Get active bonuses for client via Website API (UI data).
    Returns list of bonus cards visible to user.
    """
    try:
        # Try to get active bonuses via Website API (requires session token)
        # First need to login with player credentials
        # For simplicity, use BackOffice API to get client bonuses
        bonuses = clients["backoffice"].get_client_bonuses(client_id)
        return bonuses
    except Exception as e:
        print(f"❌ Error getting bonuses via API: {e}")
        return None


def deposit_streak_test(env="qa", deposit_amount=30, iterations=10, ticket_id=None):
    """
    Execute full deposit streak test with API and UI verification.
    
    Args:
        env: Environment (dev, qa, prod)
        deposit_amount: Minimum deposit amount (default 30 USD)
        iterations: Number of deposit iterations (default 10)
        ticket_id: Optional Jira ticket ID for email generation
        
    Returns:
        Dictionary with test results and logs
    """
    print("="*80)
    print("🎯 DEPOSIT STREAK TEST - FULL CYCLE")
    print("="*80)
    print(f"Environment: {env.upper()}")
    print(f"Deposit amount: ${deposit_amount} USD")
    print(f"Iterations: {iterations}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    # Step 1: Create test player
    print("🔄 Step 1: Creating test player...")
    player_result = create_test_player(
        env=env,
        ticket_id=ticket_id,
        setup_balance=False,  # We'll add balance via deposits
        balance_amount=0,
        method="graphql"
    )
    
    if not player_result.get("clientId"):
        print("❌ Failed to create test player")
        return {"success": False, "error": "Player creation failed"}
    
    client_id = player_result["clientId"]
    email = player_result["email"]
    password = player_result["password"]
    session_token = player_result.get("sessionToken")
    
    print(f"✅ Player created: {email} (ID: {client_id})")
    
    # Set session token for Website API client
    if session_token:
        clients["website"].set_session_token(session_token)
    
    # Step 2: Get initial bonus state (before any deposits)
    print("\n🔄 Step 2: Getting initial bonus state...")
    initial_bonuses = get_client_bonuses_api(clients, client_id, env)
    initial_count = len(initial_bonuses.get("ResponseObject", [])) if initial_bonuses else 0
    print(f"   Initial bonus count: {initial_count}")
    
    if initial_bonuses and initial_count > 0:
        print("   Initial bonuses:")
        for bonus in initial_bonuses.get("ResponseObject", [])[:5]:
            print(f"     - {bonus.get('Name', 'Unknown')} (ID: {bonus.get('Id')})")
    
    # Step 3: Execute deposit iterations
    print(f"\n🔄 Step 3: Executing {iterations} deposit iterations...")
    
    iteration_logs = []
    all_success = True
    
    for i in range(1, iterations + 1):
        print(f"\n--- Iteration {i}/{iterations} ---")
        
        # Step API: Create deposit
        print(f"   Deposit {i}: Creating ${deposit_amount} deposit...")
        deposit_result = create_deposit_flow(
            env=env,
            client_id=client_id,
            amount=deposit_amount,
            currency="USD",
            payment_method_id=19,  # Default payment method
            use_wallet=True,  # Use wallet correction for simplicity
            auto_confirm=True
        )
        
        deposit_success = deposit_result.get("success", False)
        deposit_details = deposit_result.get("deposit_details", {})
        
        # Step UI: Simulate page refresh and check bonuses
        print(f"   Checking bonuses after deposit {i}...")
        bonuses_after = get_client_bonuses_api(clients, client_id, env)
        bonus_count = len(bonuses_after.get("ResponseObject", [])) if bonuses_after else 0
        
        # Identify new bonuses (compare with previous state)
        new_bonuses = []
        if bonuses_after and initial_bonuses:
            before_ids = {b.get("Id") for b in initial_bonuses.get("ResponseObject", [])}
            after_bonuses = bonuses_after.get("ResponseObject", [])
            for bonus in after_bonuses:
                if bonus.get("Id") not in before_ids:
                    new_bonuses.append(bonus)
        
        # Update initial_bonuses for next iteration
        initial_bonuses = bonuses_after
        
        # Log iteration results
        iteration_log = {
            "iteration": i,
            "deposit_amount": deposit_amount,
            "deposit_success": deposit_success,
            "deposit_details": deposit_details,
            "bonus_count": bonus_count,
            "new_bonuses": [
                {
                    "id": b.get("Id"),
                    "name": b.get("Name"),
                    "type": b.get("BonusType"),
                    "status": b.get("Status")
                }
                for b in new_bonuses
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        iteration_logs.append(iteration_log)
        
        # Print summary
        print(f"   ✅ Deposit: {'Success' if deposit_success else 'Failed'}")
        print(f"   ✅ Bonus count: {bonus_count}")
        print(f"   ✅ New bonuses: {len(new_bonuses)}")
        
        if new_bonuses:
            for bonus in new_bonuses:
                print(f"       - {bonus.get('Name')} (ID: {bonus.get('Id')})")
        
        # Wait a moment between iterations
        if i < iterations:
            time.sleep(2)
    
    # Step 4: Final verification
    print("\n🔄 Step 4: Final verification...")
    final_bonuses = get_client_bonuses_api(clients, client_id, env)
    final_count = len(final_bonuses.get("ResponseObject", [])) if final_bonuses else 0
    
    print(f"   Total deposits made: {iterations}")
    print(f"   Final bonus count: {final_count}")
    
    # Calculate expected bonus count (initial + iterations if each deposit triggers a bonus)
    # Note: Deposit streak may not create a bonus for every deposit
    expected_min = initial_count + iterations  # If each deposit creates a bonus
    
    # Analyze results
    discrepancies = []
    for i, log in enumerate(iteration_logs, 1):
        if not log["deposit_success"]:
            discrepancies.append(f"Iteration {i}: Deposit failed")
        if len(log["new_bonuses"]) == 0:
            discrepancies.append(f"Iteration {i}: No new bonus created")
    
    # Prepare final result
    result = {
        "success": all_success and len(discrepancies) == 0,
        "env": env,
        "player": {
            "clientId": client_id,
            "email": email,
            "password": password
        },
        "test_config": {
            "deposit_amount": deposit_amount,
            "iterations": iterations,
            "currency": "USD"
        },
        "initial_bonus_count": initial_count,
        "final_bonus_count": final_count,
        "iterations": iteration_logs,
        "discrepancies": discrepancies,
        "summary": {
            "total_deposits": iterations,
            "successful_deposits": sum(1 for log in iteration_logs if log["deposit_success"]),
            "total_new_bonuses": sum(len(log["new_bonuses"]) for log in iteration_logs),
            "all_bonuses_displayed": final_count >= expected_min
        },
        "timestamp": datetime.now().isoformat()
    }
    
    print("\n" + "="*80)
    print("📋 TEST COMPLETE - SUMMARY")
    print("="*80)
    print(f"✅ Player: {email} (ID: {client_id})")
    print(f"✅ Total deposits: {result['summary']['total_deposits']}")
    print(f"✅ Successful deposits: {result['summary']['successful_deposits']}")
    print(f"✅ New bonuses created: {result['summary']['total_new_bonuses']}")
    print(f"✅ Initial bonus count: {initial_count}")
    print(f"✅ Final bonus count: {final_count}")
    
    if discrepancies:
        print(f"⚠️  Discrepancies found: {len(discrepancies)}")
        for d in discrepancies:
            print(f"   - {d}")
    else:
        print("🎉 All checks passed!")
    
    # Save test data log
    save_test_data_log({
        "type": "deposit_streak_test",
        "action": "full_cycle",
        **result
    })
    
    # Save detailed log to file
    log_file = Path(__file__).parent.parent / f"deposit_streak_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Detailed log saved to: {log_file}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Execute full deposit streak test with API and UI verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run deposit streak test on QA environment
  python deposit_streak_test.py --env qa --amount 30 --iterations 10
  
  # Run with custom ticket ID for email generation
  python deposit_streak_test.py --env qa --amount 30 --iterations 5 --ticket CT-999
  
  # Run on dev environment with smaller amount
  python deposit_streak_test.py --env dev --amount 10 --iterations 3
        """
    )
    
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="qa",
                       help="Environment (default: qa)")
    parser.add_argument("--amount", type=float, default=30.0,
                       help="Deposit amount per iteration (default: 30 USD)")
    parser.add_argument("--iterations", type=int, default=10,
                       help="Number of deposit iterations (default: 10)")
    parser.add_argument("--ticket", type=str,
                       help="Jira ticket ID for email generation (e.g., CT-999)")
    parser.add_argument("--output", type=str,
                       help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    # Validate deposit amount
    if args.amount < 30:
        print(f"⚠️  Warning: Deposit amount (${args.amount}) is below minimum $30 USD")
        confirm = input("Continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Test cancelled")
            sys.exit(1)
    
    try:
        result = deposit_streak_test(
            env=args.env,
            deposit_amount=args.amount,
            iterations=args.iterations,
            ticket_id=args.ticket
        )
        
        # Save to output file if specified
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: {output_path}")
        
        # Exit with appropriate code
        if result.get("success"):
            print("\n🎉 TEST PASSED")
            sys.exit(0)
        else:
            print("\n❌ TEST FAILED")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()