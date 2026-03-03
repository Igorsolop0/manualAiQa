#!/usr/bin/env python3
"""
Deposit Streak Test v3 - Corrected with BackOffice deposit flow and GraphQL checks.
Uses proper deposit flow (MakeManualRedirectPayment -> MarkAsPaid) to trigger bonus events.
Checks bonuses after every 2nd deposit (2,4,8,10) via GraphQL.
"""

import argparse
import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime


def run_script(script_name, args_list):
    """Run a Python script and return parsed JSON output."""
    script_path = Path(__file__).parent / script_name
    cmd = ["python3", str(script_path)] + args_list
    
    print(f"   Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Try to parse JSON output from stdout
        if result.stdout.strip():
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                # Script might have printed non-JSON output
                return {"raw_output": result.stdout.strip()}
        else:
            return {"success": True, "no_output": True}
            
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Script failed: {e}")
        print(f"   Stderr: {e.stderr}")
        return {"success": False, "error": e.stderr}


def get_eligible_bonuses_graphql(clients, session_token=None):
    """
    Get eligible bonuses via GraphQL query.
    
    Query:
    query EligibleBonuses {
      eligibleBonuses {
        id
        isAvailable
        hasDepositTrigger
        bmsBonusId
        bonusActivationId
        amount
        hasFreeSpins
        nextAvailableAt
        previousAvailableAt
        lastClaimedAt
        hasWagering
        isPendingCalculation
        __typename
      }
    }
    """
    try:
        url = f"{clients['graphql'].base_url}/graphql"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "website-locale": "en",
            "website-origin": f"https://minebit-casino.prod.sofon.one",
        }
        
        if session_token:
            headers["Authorization"] = session_token
        
        query = """
        query EligibleBonuses {
          eligibleBonuses {
            id
            isAvailable
            hasDepositTrigger
            bmsBonusId
            bonusActivationId
            amount
            hasFreeSpins
            nextAvailableAt
            previousAvailableAt
            lastClaimedAt
            hasWagering
            isPendingCalculation
            __typename
          }
        }
        """
        
        data = {"query": query}
        
        import requests
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if "errors" in result:
            print(f"⚠️  GraphQL errors: {result['errors']}")
            return None
            
        return result.get("data", {}).get("eligibleBonuses", [])
        
    except Exception as e:
        print(f"❌ GraphQL query failed: {e}")
        return None


def get_bonus_details_graphql(clients, bonus_id, session_token=None):
    """
    Get bonus details via GraphQL query.
    
    Query:
    query BonusDetails($id: ID!) {
      bonusDetails(id: $id) {
        id
        name
        validTill
        availableInProducts
        turnOverCount
        __typename
      }
    }
    """
    try:
        url = f"{clients['graphql'].base_url}/graphql"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "website-locale": "en",
            "website-origin": f"https://minebit-casino.prod.sofon.one",
        }
        
        if session_token:
            headers["Authorization"] = session_token
        
        query = """
        query BonusDetails($id: ID!) {
          bonusDetails(id: $id) {
            id
            name
            validTill
            availableInProducts
            turnOverCount
            __typename
          }
        }
        """
        
        variables = {"id": bonus_id}
        data = {"query": query, "variables": variables}
        
        import requests
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if "errors" in result:
            print(f"⚠️  GraphQL errors: {result['errors']}")
            return None
            
        return result.get("data", {}).get("bonusDetails")
        
    except Exception as e:
        print(f"❌ GraphQL bonus details failed: {e}")
        return None


def deposit_streak_test_v3(env="prod", deposit_amount=30, iterations=10, ticket_id=None):
    """
    Execute corrected deposit streak test with proper deposit flow.
    
    Args:
        env: Environment (dev, qa, prod)
        deposit_amount: Minimum deposit amount (default 30 USD)
        iterations: Number of deposit iterations (default 10)
        ticket_id: Optional Jira ticket ID for email generation
        
    Returns:
        Dictionary with test results and logs
    """
    print("="*80)
    print("🎯 DEPOSIT STREAK TEST v3 - CORRECTED FLOW")
    print("="*80)
    print(f"Environment: {env.upper()}")
    print(f"Deposit amount: ${deposit_amount} USD")
    print(f"Iterations: {iterations}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Import API clients dynamically to avoid circular imports
    sys.path.insert(0, str(Path(__file__).parent))
    from api_clients import ApiClientFactory
    
    # Create API clients
    clients = ApiClientFactory.create_clients(env)
    
    # Step 1: Create test player via GraphQL (to get session token)
    print("🔄 Step 1: Creating test player via GraphQL...")
    
    import subprocess
    import json as json_module
    
    player_args = ["--env", env, "--no-balance", "--method", "graphql"]
    if ticket_id:
        player_args.extend(["--ticket", ticket_id])
    
    script_path = Path(__file__).parent / "01_create_test_player.py"
    cmd = ["python3", str(script_path)] + player_args
    
    print(f"   Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    # Read player data from default output file
    last_player_file = Path(__file__).parent.parent / "last_player.json"
    if not last_player_file.exists():
        print("❌ Player creation failed - no output file")
        print(f"   Output: {result.stdout}")
        print(f"   Error: {result.stderr}")
        return {"success": False, "error": "Player creation failed"}
    
    with open(last_player_file, "r") as f:
        player_result = json_module.load(f)
    
    if not player_result.get("success", True):
        print("❌ Failed to create test player")
        return {"success": False, "error": "Player creation failed"}
    
    client_id = player_result.get("clientId")
    email = player_result.get("email")
    password = player_result.get("password")
    session_token = player_result.get("sessionToken")
    
    if not client_id:
        print("❌ No client ID in player result")
        return {"success": False, "error": "No client ID"}
    
    print(f"✅ Player created: {email} (ID: {client_id})")
    if session_token:
        print(f"✅ Session token obtained ({session_token[:20]}...)")
    
    # Step 2: Get initial bonuses state via GraphQL
    print("\n🔄 Step 2: Getting initial bonus state via GraphQL...")
    initial_bonuses = get_eligible_bonuses_graphql(clients, session_token)
    initial_count = len(initial_bonuses) if initial_bonuses else 0
    
    print(f"   Initial bonus count: {initial_count}")
    if initial_bonuses:
        for bonus in initial_bonuses[:5]:
            print(f"     - {bonus.get('id')}: {bonus.get('name', 'Unknown')}")
    
    # Step 3: Execute deposit iterations with BackOffice flow
    print(f"\n🔄 Step 3: Executing {iterations} deposit iterations (BackOffice flow)...")
    
    iteration_logs = []
    bonus_checkpoints = [2, 4, 8, 10]  # Check after these deposits
    bonus_history = []  # Track bonuses that appear
    
    for i in range(1, iterations + 1):
        print(f"\n--- Iteration {i}/{iterations} ---")
        
        # Step API: Create deposit via BackOffice (NOT Wallet correction)
        print(f"   Deposit {i}: Creating ${deposit_amount} deposit via BackOffice...")
        deposit_args = [
            "--env", env,
            "--amount", str(deposit_amount),
            "--currency", "USD",
            # No --use-wallet flag = use BackOffice flow
            "--auto-confirm",
            "--output", "-",
            str(client_id)
        ]
        
        script_path = Path(__file__).parent / "03_create_deposit_flow.py"
        cmd = ["python3", str(script_path)] + deposit_args
        
        print(f"   Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        # Parse deposit result
        deposit_success = False
        deposit_result = {}
        
        # Try to parse JSON from stdout
        if result.stdout.strip():
            try:
                deposit_result = json_module.loads(result.stdout)
                deposit_success = deposit_result.get("success", False)
            except json_module.JSONDecodeError:
                # Check for success in output text
                if "Deposit flow completed successfully" in result.stdout:
                    deposit_success = True
                else:
                    print(f"   ❌ Could not parse deposit result")
        
        # Check bonuses via GraphQL after every 2nd deposit
        bonuses_after = None
        bonus_count = 0
        new_bonuses = []
        
        if i in bonus_checkpoints:
            print(f"   🔍 Checking bonuses after deposit {i} (checkpoint)...")
            time.sleep(3)  # Wait for bonus calculation
            
            bonuses_after = get_eligible_bonuses_graphql(clients, session_token)
            if bonuses_after is not None:
                bonus_count = len(bonuses_after)
                
                # Identify new bonuses compared to previous checkpoint
                previous_bonus_ids = {b["id"] for b in bonus_history}
                current_bonus_ids = {b["id"] for b in bonuses_after}
                new_bonus_ids = current_bonus_ids - previous_bonus_ids
                
                for bonus in bonuses_after:
                    if bonus["id"] in new_bonus_ids:
                        new_bonuses.append(bonus)
                        bonus_history.append(bonus)
                        
                        # Get bonus details
                        details = get_bonus_details_graphql(clients, bonus["bmsBonusId"], session_token)
                        if details:
                            bonus["details"] = details
        else:
            print(f"   ⏭️  Skipping bonus check (not a checkpoint)")
        
        # Log iteration results
        iteration_log = {
            "iteration": i,
            "deposit_amount": deposit_amount,
            "deposit_success": deposit_success,
            "bonus_count": bonus_count,
            "new_bonuses": [
                {
                    "id": b.get("id"),
                    "bmsBonusId": b.get("bmsBonusId"),
                    "amount": b.get("amount"),
                    "isAvailable": b.get("isAvailable"),
                    "name": b.get("details", {}).get("name") if "details" in b else None
                }
                for b in new_bonuses
            ],
            "checkpoint": i in bonus_checkpoints,
            "timestamp": datetime.now().isoformat()
        }
        
        iteration_logs.append(iteration_log)
        
        # Print summary
        print(f"   ✅ Deposit: {'Success' if deposit_success else 'Failed'}")
        if i in bonus_checkpoints:
            print(f"   ✅ Bonus count: {bonus_count}")
            print(f"   ✅ New bonuses: {len(new_bonuses)}")
            for bonus in new_bonuses:
                name = bonus.get("details", {}).get("name") if "details" in bonus else "Unknown"
                print(f"       - {name} (ID: {bonus.get('id')}, Amount: ${bonus.get('amount', 0)})")
        
        # Wait a moment between iterations
        if i < iterations:
            time.sleep(2)
    
    # Step 4: Final verification
    print("\n🔄 Step 4: Final verification...")
    final_bonuses = get_eligible_bonuses_graphql(clients, session_token)
    final_count = len(final_bonuses) if final_bonuses else 0
    
    print(f"   Total deposits made: {iterations}")
    print(f"   Final bonus count: {final_count}")
    print(f"   Expected bonuses at checkpoints: {len(bonus_checkpoints)}")
    
    # Calculate success rate
    successful_deposits = sum(1 for log in iteration_logs if log["deposit_success"])
    total_new_bonuses = sum(len(log["new_bonuses"]) for log in iteration_logs)
    
    # Analyze results
    discrepancies = []
    
    # Check if we got bonuses at each checkpoint
    for checkpoint in bonus_checkpoints:
        iteration_log = next((log for log in iteration_logs if log["iteration"] == checkpoint), None)
        if iteration_log:
            if len(iteration_log["new_bonuses"]) == 0:
                discrepancies.append(f"Iteration {checkpoint}: Expected bonus but none appeared")
        else:
            discrepancies.append(f"Iteration {checkpoint}: Missing log entry")
    
    # Prepare final result
    result = {
        "success": successful_deposits == iterations and total_new_bonuses >= len(bonus_checkpoints),
        "env": env,
        "player": {
            "clientId": client_id,
            "email": email,
            "password": password,
            "sessionToken": session_token[:20] + "..." if session_token else None
        },
        "test_config": {
            "deposit_amount": deposit_amount,
            "iterations": iterations,
            "currency": "USD",
            "bonus_checkpoints": bonus_checkpoints,
            "deposit_method": "BackOffice flow (MakeManualRedirectPayment -> MarkAsPaid)"
        },
        "initial_bonus_count": initial_count,
        "final_bonus_count": final_count,
        "iterations": iteration_logs,
        "discrepancies": discrepancies,
        "summary": {
            "total_deposits": iterations,
            "successful_deposits": successful_deposits,
            "total_new_bonuses": total_new_bonuses,
            "expected_bonuses": len(bonus_checkpoints),
            "deposit_success_rate": f"{successful_deposits}/{iterations}",
            "bonus_success_rate": f"{total_new_bonuses}/{len(bonus_checkpoints)}"
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
    print(f"✅ Expected bonuses at checkpoints: {result['summary']['expected_bonuses']}")
    print(f"✅ Initial bonus count: {initial_count}")
    print(f"✅ Final bonus count: {final_count}")
    
    if discrepancies:
        print(f"⚠️  Discrepancies found: {len(discrepancies)}")
        for d in discrepancies:
            print(f"   - {d}")
    else:
        print("🎉 All checks passed!")
    
    # Save detailed log to file
    log_file = Path(__file__).parent.parent / f"deposit_streak_v3_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w") as f:
        json_module.dump(result, f, indent=2)
    print(f"\n💾 Detailed log saved to: {log_file}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Execute corrected deposit streak test with BackOffice flow and GraphQL checks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run corrected deposit streak test on PROD
  python deposit_streak_test3.py --env prod --amount 30 --iterations 10
  
  # Run with custom ticket ID
  python deposit_streak_test3.py --env prod --amount 30 --iterations 10 --ticket CT-999
        """
    )
    
    parser.add_argument("--env", choices=["dev", "qa", "prod"], default="prod",
                       help="Environment (default: prod)")
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
        result = deposit_streak_test_v3(
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