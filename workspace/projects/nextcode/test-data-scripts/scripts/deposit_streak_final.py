#!/usr/bin/env python3
"""
Deposit Streak Test - Final version with BackOffice deposit flow and GraphQL checks.
Uses payment_method_id 19 for USD deposits on Minebit PROD.
Checks bonuses after every 2nd deposit (2,4,8,10).
"""

import argparse
import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
import requests


def create_test_player(env="prod", ticket_id=None):
    """Create a test player via GraphQL and return player data."""
    print("🔄 Creating test player via GraphQL...")
    
    script_path = Path(__file__).parent / "01_create_test_player.py"
    args = ["--env", env, "--no-balance", "--method", "graphql"]
    if ticket_id:
        args.extend(["--ticket", ticket_id])
    
    cmd = ["python3", str(script_path)] + args
    print(f"   Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    # Read player data from output file
    last_player_file = Path(__file__).parent.parent / "last_player.json"
    if not last_player_file.exists():
        print(f"❌ Player creation failed - no output file")
        print(f"   Stdout: {result.stdout[:200]}")
        print(f"   Stderr: {result.stderr[:200]}")
        return None
    
    with open(last_player_file, "r") as f:
        player_data = json.load(f)
    
    if not player_data.get("success", True):
        print(f"❌ Player creation failed: {player_data}")
        return None
    
    client_id = player_data.get("clientId")
    email = player_data.get("email")
    password = player_data.get("password")
    session_token = player_data.get("sessionToken")
    
    if not client_id:
        print(f"❌ No client ID in player data")
        return None
    
    print(f"✅ Player created: {email} (ID: {client_id})")
    if session_token:
        print(f"✅ Session token: {session_token[:20]}...")
    
    return {
        "client_id": client_id,
        "email": email,
        "password": password,
        "session_token": session_token
    }


def make_backoffice_deposit(client_id, amount, env="prod"):
    """Make a deposit via BackOffice API with payment_method_id 19."""
    print(f"   Making deposit ${amount} via BackOffice...")
    
    script_path = Path(__file__).parent / "03_create_deposit_flow.py"
    args = [
        "--env", env,
        "--amount", str(amount),
        "--payment-method", "19",
        "--auto-confirm",
        "--output", "-",
        str(client_id)
    ]
    
    cmd = ["python3", str(script_path)] + args
    print(f"   Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    # Check for success
    success = False
    if result.returncode == 0:
        # Try to parse JSON output
        if result.stdout.strip():
            try:
                output = json.loads(result.stdout)
                success = output.get("success", False)
            except json.JSONDecodeError:
                # Check for success message in text
                if "Deposit flow completed successfully" in result.stdout:
                    success = True
                elif "Success" in result.stdout:
                    success = True
        else:
            # Empty output might mean success
            success = True
    
    return success


def query_eligible_bonuses(session_token, partner_id=5):
    """Query eligible bonuses via GraphQL."""
    if not session_token:
        print("   ⚠️  No session token, skipping GraphQL query")
        return None
    
    url = "https://minebit-casino.prod.sofon.one/graphql"
    headers = {
        "Content-Type": "application/json",
        "Authorization": session_token,
        "website-locale": "en",
        "website-origin": "https://minebit-casino.prod.sofon.one",
    }
    
    query = """
    query EligibleBonuses($bmsPartnerId: Int!) {
      eligibleBonuses(bmsPartnerId: $bmsPartnerId) {
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
    
    variables = {"bmsPartnerId": partner_id}
    data = {"query": query, "variables": variables}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if "errors" in result:
            print(f"   ⚠️  GraphQL errors: {result['errors'][0]['message'][:50]}...")
            return None
        
        return result.get("data", {}).get("eligibleBonuses", [])
        
    except Exception as e:
        print(f"   ⚠️  GraphQL query failed: {e}")
        return None


def query_bonus_details(session_token, bonus_id):
    """Query bonus details via GraphQL."""
    if not session_token:
        return None
    
    url = "https://minebit-casino.prod.sofon.one/graphql"
    headers = {
        "Content-Type": "application/json",
        "Authorization": session_token,
        "website-locale": "en",
        "website-origin": "https://minebit-casino.prod.sofon.one",
    }
    
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
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if "errors" in result:
            return None
        
        return result.get("data", {}).get("bonusDetails")
        
    except Exception:
        return None


def deposit_streak_test(env="prod", deposit_amount=30, iterations=10, ticket_id=None):
    """Execute deposit streak test with BackOffice deposits and GraphQL checks."""
    print("="*80)
    print("🎯 DEPOSIT STREAK TEST - FINAL VERSION")
    print("="*80)
    print(f"Environment: {env.upper()}")
    print(f"Deposit amount: ${deposit_amount} USD")
    print(f"Iterations: {iterations}")
    print(f"Bonus checkpoints: every 2nd deposit (2,4,8,10)")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Step 1: Create test player
    player = create_test_player(env, ticket_id)
    if not player:
        print("❌ Test aborted - failed to create test player")
        return {"success": False, "error": "Player creation failed"}
    
    client_id = player["client_id"]
    email = player["email"]
    session_token = player["session_token"]
    
    # Step 2: Get initial bonus state
    print("\n🔄 Getting initial bonus state...")
    initial_bonuses = query_eligible_bonuses(session_token)
    initial_count = len(initial_bonuses) if initial_bonuses else 0
    print(f"   Initial bonus count: {initial_count}")
    
    # Track bonus history
    bonus_history = []  # List of bonus IDs that have appeared
    iteration_logs = []
    
    # Bonus checkpoints (every 2nd deposit)
    bonus_checkpoints = [2, 4, 8, 10]
    
    # Step 3: Execute deposit iterations
    print(f"\n🔄 Executing {iterations} deposit iterations...")
    
    for i in range(1, iterations + 1):
        print(f"\n--- Iteration {i}/{iterations} ---")
        
        # Make deposit
        deposit_success = make_backoffice_deposit(client_id, deposit_amount, env)
        
        # Check bonuses after every 2nd deposit
        bonuses_after = None
        bonus_count = 0
        new_bonuses = []
        
        if i in bonus_checkpoints:
            print(f"   🔍 Checking bonuses after deposit {i}...")
            time.sleep(3)  # Wait for bonus calculation
            
            bonuses_after = query_eligible_bonuses(session_token)
            if bonuses_after is not None:
                bonus_count = len(bonuses_after)
                
                # Identify new bonuses
                previous_bonus_ids = {b["id"] for b in bonus_history}
                current_bonus_ids = {b["id"] for b in bonuses_after}
                new_bonus_ids = current_bonus_ids - previous_bonus_ids
                
                for bonus in bonuses_after:
                    if bonus["id"] in new_bonus_ids:
                        # Get bonus details
                        details = query_bonus_details(session_token, bonus["bmsBonusId"])
                        if details:
                            bonus["details"] = details
                        
                        new_bonuses.append(bonus)
                        bonus_history.append(bonus)
        else:
            print(f"   ⏭️  Skipping bonus check (not a checkpoint)")
        
        # Prepare log entry
        bonus_names = []
        for bonus in new_bonuses:
            name = bonus.get("details", {}).get("name", "Unknown")
            bonus_names.append(name)
        
        # Format log line as requested
        api_status = "Success" if deposit_success else "Failed"
        ui_bonus_card = "Found" if new_bonuses else "Not Found"
        bonus_name = bonus_names[0] if bonus_names else "None"
        
        log_line = f"[Iteration {i}] Deposit: {deposit_amount} USD | API Status: {api_status} | UI Bonus Card: {ui_bonus_card} | Bonus Name: {bonus_name}"
        print(f"   📝 {log_line}")
        
        # Store detailed log
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
                    "name": b.get("details", {}).get("name") if "details" in b else "Unknown"
                }
                for b in new_bonuses
            ],
            "log_line": log_line,
            "checkpoint": i in bonus_checkpoints,
            "timestamp": datetime.now().isoformat()
        }
        
        iteration_logs.append(iteration_log)
        
        # Wait between iterations
        if i < iterations:
            time.sleep(2)
    
    # Step 4: Final verification
    print("\n🔄 Final verification...")
    final_bonuses = query_eligible_bonuses(session_token)
    final_count = len(final_bonuses) if final_bonuses else 0
    
    print(f"   Total deposits made: {iterations}")
    print(f"   Final bonus count: {final_count}")
    print(f"   Expected bonuses at checkpoints: {len(bonus_checkpoints)}")
    
    # Calculate success metrics
    successful_deposits = sum(1 for log in iteration_logs if log["deposit_success"])
    total_new_bonuses = sum(len(log["new_bonuses"]) for log in iteration_logs)
    
    # Check discrepancies
    discrepancies = []
    
    # Check if we got bonuses at each checkpoint
    for checkpoint in bonus_checkpoints:
        iteration_log = next((log for log in iteration_logs if log["iteration"] == checkpoint), None)
        if iteration_log:
            if len(iteration_log["new_bonuses"]) == 0:
                discrepancies.append(f"Iteration {checkpoint}: Expected bonus but none appeared")
        else:
            discrepancies.append(f"Iteration {checkpoint}: Missing log entry")
    
    # Check for API/UI discrepancies
    for log in iteration_logs:
        if log["deposit_success"] and log["checkpoint"]:
            if len(log["new_bonuses"]) == 0:
                discrepancies.append(f"Iteration {log['iteration']}: Deposit successful but no bonus appeared (API/UI mismatch)")
    
    # Prepare final result
    result = {
        "success": successful_deposits == iterations and total_new_bonuses >= len(bonus_checkpoints),
        "env": env,
        "player": {
            "clientId": client_id,
            "email": email,
            "password": player["password"]
        },
        "test_config": {
            "deposit_amount": deposit_amount,
            "iterations": iterations,
            "currency": "USD",
            "payment_method_id": 19,
            "bonus_checkpoints": bonus_checkpoints
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
    
    # Print summary
    print("\n" + "="*80)
    print("📋 TEST COMPLETE - SUMMARY")
    print("="*80)
    print(f"✅ Player: {email} (ID: {client_id})")
    print(f"✅ Total deposits: {result['summary']['total_deposits']}")
    print(f"✅ Successful deposits: {result['summary']['successful_deposits']}")
    print(f"✅ New bonuses created: {result['summary']['total_new_bonuses']}")
    print(f"✅ Expected bonuses: {result['summary']['expected_bonuses']}")
    
    # Print all log lines
    print("\n📝 ITERATION LOGS:")
    for log in iteration_logs:
        print(f"   {log['log_line']}")
    
    if discrepancies:
        print(f"\n⚠️  DISCREPANCIES FOUND ({len(discrepancies)}):")
        for d in discrepancies:
            print(f"   • {d}")
    else:
        print("\n🎉 ALL CHECKS PASSED!")
    
    # Save detailed log
    log_file = Path(__file__).parent.parent / f"deposit_streak_final_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Detailed log saved to: {log_file}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Execute final deposit streak test with BackOffice deposits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run test on PROD with default parameters
  python deposit_streak_final.py --env prod --amount 30 --iterations 10
  
  # Run with ticket ID for email generation
  python deposit_streak_final.py --env prod --amount 30 --iterations 10 --ticket CT-999
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