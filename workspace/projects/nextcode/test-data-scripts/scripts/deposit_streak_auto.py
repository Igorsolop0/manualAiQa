#!/usr/bin/env python3
"""
Deposit Streak Automated Test with BackOffice UI API (Bearer token).
Full flow: Create deposit -> Find PaymentRequestId -> MarkAsPaid -> Check bonuses.
"""

import argparse
import json
import sys
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta
import subprocess


class BackOfficeUIApiClient:
    """Client for BackOffice UI API (Bearer token auth)."""
    
    def __init__(self, base_url: str, bearer_token: str, partner_id: int = 5):
        """
        Initialize BackOffice UI API client.
        
        Args:
            base_url: Base URL (e.g., https://backoffice.prod.sofon.one)
            bearer_token: Bearer token for authentication
            partner_id: Partner ID (default: 5 for Minebit)
        """
        self.base_url = base_url.rstrip("/")
        self.bearer_token = bearer_token
        self.partner_id = partner_id
        
        # Common headers for BackOffice UI API
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,de;q=0.7",
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
            "X-Partner-ID": str(partner_id),
            "Origin": self.base_url,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        }
    
    def create_deposit(self, client_id: int, amount: float, currency: str = "USD", 
                       payment_method_id: int = 19) -> dict:
        """
        Create deposit via MakeManualRedirectPayment.
        
        Args:
            client_id: Client ID
            amount: Deposit amount
            currency: Currency code
            payment_method_id: Payment method ID (19 for USD test)
            
        Returns:
            Deposit creation response
        """
        url = f"{self.base_url}/mgw/admin/api/Client/MakeManualRedirectPayment?TimeZone=1&LanguageId=en"
        
        data = {
            "amount": amount,
            "clientId": client_id,
            "currencyId": currency,
            "externalTransactionId": f"test_{int(time.time())}_{client_id}",
            "partnerPaymentMethodId": payment_method_id,
            "paymentRequestType": "Deposit"
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ResponseCode") != "Success":
            raise Exception(f"Deposit creation failed: {result}")
        
        return result
    
    def find_deposit_id(self, client_id: int, external_transaction_id: str = None, max_attempts: int = 5) -> int:
        """
        Find PaymentRequestId for the latest deposit of a client.
        
        Args:
            client_id: Client ID
            external_transaction_id: Optional external transaction ID to match
            max_attempts: Maximum attempts to find the deposit
            
        Returns:
            PaymentRequestId (int) or None if not found
        """
        url = f"{self.base_url}/mgw/admin/api/v2/Payment/GetAllWithTotal?TimeZone=1&LanguageId=en"
        
        # Date range: last 7 days
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00.000Z")
        to_date = datetime.utcnow().strftime("%Y-%m-%dT23:59:59.999Z")
        
        filter_data = {
            "TakeCount": 50,
            "SkipCount": 0,
            "OrderBy": 0,  # 0 = descending by UpdatedAt
            "FieldNameToOrderBy": "UpdatedAt",
            "FromDate": from_date,
            "ToDate": to_date,
            "Types": ["Deposit"],
            "Partners": [self.partner_id],
            "Clients": [client_id]
        }
        
        for attempt in range(max_attempts):
            time.sleep(2)  # Wait for deposit to appear
            
            response = requests.post(url, json=filter_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("ResponseCode") != "Success":
                print(f"⚠️  GetAllWithTotal failed: {result.get('Description')}")
                continue
            
            payments = result.get("ResponseObject", {}).get("Payments", [])
            
            if not payments:
                print(f"⚠️  No deposits found for client {client_id} (attempt {attempt + 1}/{max_attempts})")
                continue
            
            # Find the latest deposit (first in list due to OrderBy descending)
            latest_deposit = payments[0]
            deposit_id = latest_deposit.get("Id")
            
            if external_transaction_id:
                # Try to match by external transaction ID
                for payment in payments:
                    if payment.get("ExternalTransactionId") == external_transaction_id:
                        deposit_id = payment.get("Id")
                        print(f"✅ Found deposit by externalTransactionId: {external_transaction_id}")
                        break
            
            if deposit_id:
                print(f"✅ Found PaymentRequestId: {deposit_id}")
                return deposit_id
        
        return None
    
    def mark_deposit_as_paid(self, payment_request_id: int, comment: str = "Test deposit") -> dict:
        """
        Mark deposit as paid via ChangeStatus.
        
        Args:
            payment_request_id: Payment request ID
            comment: Comment for the status change
            
        Returns:
            Status change response
        """
        url = f"{self.base_url}/mgw/admin/api/v2/Payment/ChangeStatus?TimeZone=1&LanguageId=en"
        
        data = {
            "Comment": comment,
            "PaymentRequestId": payment_request_id,
            "ChangeStatusTo": "MarkAsPaid",
            "ProcessingType": 0,
            "Type": "Deposit"
        }
        
        # Add Referer header for this specific request
        headers = self.headers.copy()
        headers["Referer"] = f"{self.base_url}/deposits/{payment_request_id}"
        
        response = requests.patch(url, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ResponseCode") != "Success":
            raise Exception(f"MarkAsPaid failed: {result}")
        
        return result
    
    def get_deposit_details(self, payment_request_id: int) -> dict:
        """
        Get deposit details by ID.
        
        Args:
            payment_request_id: Payment request ID
            
        Returns:
            Deposit details
        """
        url = f"{self.base_url}/mgw/admin/api/v2/Payment/GetById/{payment_request_id}?TimeZone=1&LanguageId=en"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ResponseCode") != "Success":
            raise Exception(f"Get deposit details failed: {result}")
        
        return result


class GraphQLClient:
    """Client for GraphQL API (Website session token)."""
    
    def __init__(self, base_url: str, session_token: str = None, partner_id: int = 5):
        self.base_url = base_url.rstrip("/")
        self.session_token = session_token
        self.partner_id = partner_id
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": session_token if session_token else "",
            "website-locale": "en",
            "website-origin": "https://minebit-casino.prod.sofon.one",
        }
    
    def query_eligible_bonuses(self) -> list:
        """Query eligible bonuses via GraphQL."""
        if not self.session_token:
            print("⚠️  No session token for GraphQL")
            return []
        
        url = f"{self.base_url}/graphql"
        
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
        
        variables = {"bmsPartnerId": self.partner_id}
        data = {"query": query, "variables": variables}
        
        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if "errors" in result:
                print(f"⚠️  GraphQL errors: {result['errors'][0]['message'][:50]}...")
                return []
            
            return result.get("data", {}).get("eligibleBonuses", [])
            
        except Exception as e:
            print(f"⚠️  GraphQL query failed: {e}")
            return []
    
    def query_bonus_details(self, bonus_id: int) -> dict:
        """Query bonus details via GraphQL."""
        if not self.session_token:
            return None
        
        url = f"{self.base_url}/graphql"
        
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
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if "errors" in result:
                return None
            
            return result.get("data", {}).get("bonusDetails")
            
        except Exception:
            return None


def deposit_streak_test(bearer_token: str, client_id: int, iterations: int = 10, 
                        deposit_amount: float = 30.0, check_bonuses: bool = False,
                        graphql_token: str = None) -> dict:
    """
    Execute deposit streak test with full automation.
    
    Args:
        bearer_token: Bearer token for BackOffice UI API
        client_id: Client ID to deposit to
        iterations: Number of deposit iterations
        deposit_amount: Amount per deposit
        check_bonuses: Whether to check bonuses via GraphQL
        graphql_token: Session token for GraphQL API
        
    Returns:
        Test results dictionary
    """
    print("="*80)
    print("🎯 DEPOSIT STREAK TEST - FULL AUTOMATION")
    print("="*80)
    print(f"Client ID: {client_id}")
    print(f"Iterations: {iterations}")
    print(f"Deposit amount: ${deposit_amount} USD")
    print(f"Bonus checkpoints: every 2nd deposit (2,4,8,10)")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Initialize clients
    backoffice_client = BackOfficeUIApiClient(
        base_url="https://backoffice.prod.sofon.one",
        bearer_token=bearer_token,
        partner_id=5
    )
    
    graphql_client = None
    if check_bonuses and graphql_token:
        graphql_client = GraphQLClient(
            base_url="https://minebit-casino.prod.sofon.one",
            session_token=graphql_token,
            partner_id=5
        )
    
    # Bonus checkpoints (every 2nd deposit)
    bonus_checkpoints = [2, 4, 8, 10]
    
    # Track results
    iteration_logs = []
    bonus_history = []
    all_bonuses = []
    
    print(f"🔄 Executing {iterations} deposit iterations...")
    
    for i in range(1, iterations + 1):
        print(f"\n--- Iteration {i}/{iterations} ---")
        
        # Step 1: Create deposit
        print(f"   💳 Creating deposit ${deposit_amount}...")
        try:
            deposit_result = backoffice_client.create_deposit(
                client_id=client_id,
                amount=deposit_amount,
                currency="USD",
                payment_method_id=19
            )
            trace_id = deposit_result.get("TraceId", "unknown")
            print(f"   ✅ Deposit created (TraceId: {trace_id[:16]}...)")
            
            # Step 2: Find PaymentRequestId
            print(f"   🔍 Finding PaymentRequestId...")
            payment_request_id = backoffice_client.find_deposit_id(client_id)
            
            if not payment_request_id:
                print(f"   ❌ Failed to find PaymentRequestId")
                iteration_logs.append({
                    "iteration": i,
                    "deposit_success": False,
                    "payment_request_id": None,
                    "mark_as_paid_success": False,
                    "error": "PaymentRequestId not found"
                })
                continue
            
            # Step 3: Mark as paid
            print(f"   ✅ Marking deposit {payment_request_id} as paid...")
            try:
                mark_result = backoffice_client.mark_deposit_as_paid(payment_request_id)
                print(f"   ✅ Deposit marked as paid")
                mark_success = True
            except Exception as e:
                print(f"   ⚠️  MarkAsPaid failed: {e}")
                mark_success = False
            
            # Step 4: Check bonuses if at checkpoint
            bonuses_found = []
            bonus_names = []
            
            if i in bonus_checkpoints and graphql_client:
                print(f"   🔍 Checking bonuses after deposit {i}...")
                time.sleep(3)  # Wait for bonus calculation
                
                eligible_bonuses = graphql_client.query_eligible_bonuses()
                if eligible_bonuses is not None:
                    # Identify new bonuses
                    previous_bonus_ids = {b["id"] for b in all_bonuses}
                    current_bonus_ids = {b["id"] for b in eligible_bonuses}
                    new_bonus_ids = current_bonus_ids - previous_bonus_ids
                    
                    for bonus in eligible_bonuses:
                        if bonus["id"] in new_bonus_ids:
                            # Get bonus details
                            details = graphql_client.query_bonus_details(bonus["bmsBonusId"])
                            if details:
                                bonus["details"] = details
                                bonus_names.append(details.get("name", "Unknown"))
                            
                            bonuses_found.append(bonus)
                            all_bonuses.append(bonus)
            
            # Prepare log line
            api_status = "Success" if deposit_result.get("ResponseCode") == "Success" else "Failed"
            ui_bonus_card = "Found" if bonuses_found else "Not Found"
            bonus_name = bonus_names[0] if bonus_names else "None"
            
            log_line = f"[Iteration {i}] Deposit: {deposit_amount} USD | API Status: {api_status} | UI Bonus Card: {ui_bonus_card} | Bonus Name: {bonus_name}"
            print(f"   📝 {log_line}")
            
            # Store detailed log
            iteration_logs.append({
                "iteration": i,
                "deposit_success": True,
                "payment_request_id": payment_request_id,
                "mark_as_paid_success": mark_success,
                "bonuses_found": bonuses_found,
                "bonus_names": bonus_names,
                "log_line": log_line,
                "checkpoint": i in bonus_checkpoints,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"   ❌ Iteration {i} failed: {e}")
            iteration_logs.append({
                "iteration": i,
                "deposit_success": False,
                "error": str(e),
                "log_line": f"[Iteration {i}] Deposit: {deposit_amount} USD | API Status: Failed | UI Bonus Card: Not Found | Bonus Name: None"
            })
        
        # Wait between iterations (except after last)
        if i < iterations:
            time.sleep(2)
    
    # Generate summary
    successful_deposits = sum(1 for log in iteration_logs if log.get("deposit_success", False))
    successful_mark_as_paid = sum(1 for log in iteration_logs if log.get("mark_as_paid_success", False))
    total_new_bonuses = sum(len(log.get("bonuses_found", [])) for log in iteration_logs)
    
    result = {
        "success": successful_deposits == iterations,
        "client_id": client_id,
        "iterations": iterations,
        "deposit_amount": deposit_amount,
        "bonus_checkpoints": bonus_checkpoints,
        "successful_deposits": successful_deposits,
        "successful_mark_as_paid": successful_mark_as_paid,
        "total_new_bonuses": total_new_bonuses,
        "expected_bonuses": len(bonus_checkpoints),
        "iteration_logs": iteration_logs,
        "summary": {
            "deposit_success_rate": f"{successful_deposits}/{iterations}",
            "mark_as_paid_success_rate": f"{successful_mark_as_paid}/{iterations}",
            "bonus_success_rate": f"{total_new_bonuses}/{len(bonus_checkpoints)}"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Print summary
    print("\n" + "="*80)
    print("📋 TEST COMPLETE - SUMMARY")
    print("="*80)
    print(f"✅ Client ID: {client_id}")
    print(f"✅ Iterations completed: {iterations}")
    print(f"✅ Successful deposits: {successful_deposits}/{iterations}")
    print(f"✅ Successful MarkAsPaid: {successful_mark_as_paid}/{iterations}")
    print(f"✅ New bonuses found: {total_new_bonuses}/{len(bonus_checkpoints)}")
    
    print("\n📝 ITERATION LOGS:")
    for log in iteration_logs:
        print(f"   {log.get('log_line', 'No log line')}")
    
    # Check discrepancies
    discrepancies = []
    for checkpoint in bonus_checkpoints:
        log = next((log for log in iteration_logs if log["iteration"] == checkpoint), None)
        if log and log["checkpoint"] and len(log.get("bonuses_found", [])) == 0:
            discrepancies.append(f"Iteration {checkpoint}: Expected bonus but none appeared")
    
    if discrepancies:
        print(f"\n⚠️  DISCREPANCIES FOUND ({len(discrepancies)}):")
        for d in discrepancies:
            print(f"   • {d}")
    else:
        print("\n🎉 ALL CHECKS PASSED!")
    
    # Save detailed log
    log_file = Path(__file__).parent.parent / f"deposit_streak_auto_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Detailed log saved to: {log_file}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Automated Deposit Streak test with BackOffice UI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run test with Bearer token (manual bonus check)
  python deposit_streak_auto.py --bearer-token YOUR_TOKEN --client-id 1179890 --iterations 10
  
  # Run with GraphQL bonus checking
  python deposit_streak_auto.py --bearer-token YOUR_TOKEN --client-id 1179890 \\
    --graphql-token SESSION_TOKEN --check-bonuses
  
  # Quick test (2 iterations)
  python deposit_streak_auto.py --bearer-token YOUR_TOKEN --client-id 1179890 --iterations 2
        """
    )
    
    parser.add_argument("--bearer-token", required=True,
                       help="Bearer token for BackOffice UI API (from browser dev tools)")
    parser.add_argument("--client-id", type=int, required=True,
                       help="Client ID to deposit to")
    parser.add_argument("--iterations", type=int, default=10,
                       help="Number of deposit iterations (default: 10)")
    parser.add_argument("--amount", type=float, default=30.0,
                       help="Deposit amount per iteration (default: 30 USD)")
    parser.add_argument("--check-bonuses", action="store_true",
                       help="Check bonuses via GraphQL (requires --graphql-token)")
    parser.add_argument("--graphql-token",
                       help="Session token for GraphQL API (from Website API login)")
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
            bearer_token=args.bearer_token,
            client_id=args.client_id,
            iterations=args.iterations,
            deposit_amount=args.amount,
            check_bonuses=args.check_bonuses,
            graphql_token=args.graphql_token
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