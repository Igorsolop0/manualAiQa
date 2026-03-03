import json
import requests
import random
import string

def make_deposit(player_id, session_token=None):
    """
    Create deposit for player via BackOffice API (QA)
    Returns True if success
    """
    # BackOffice QA URL
    base_url = "https://adminwebapi.qa.sofon.one"
    headers = {
        "Content-Type": "application/json",
        "UserId": "1",  # QA admin user ID
    }
    
    # 1. Create deposit request
    deposit_url = f"{base_url}/api/Client/MakeManualRedirectPayment"
    
    # Generate random external transaction ID
    external_tx_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    
    deposit_data = {
        "amount": 100.0,
        "clientId": player_id,
        "currencyId": "USD",
        "externalTransactionId": external_tx_id,
        "partnerPaymentMethodId": 19,  # From memory
        "paymentRequestType": "Deposit"
    }
    
    print(f"Creating deposit for player {player_id}...")
    resp = requests.post(deposit_url, headers=headers, json=deposit_data)
    if resp.status_code != 200:
        print(f"Deposit creation failed: {resp.status_code} - {resp.text}")
        return False
    
    deposit_result = resp.json()
    print(f"Deposit response: {json.dumps(deposit_result, indent=2)}")
    
    # Extract payment request ID
    payment_request_id = deposit_result.get("paymentRequestId")
    if not payment_request_id:
        print("No paymentRequestId in response")
        return False
    
    print(f"Payment request ID: {payment_request_id}")
    
    # 2. Mark as paid
    mark_paid_url = f"{base_url}/api/Payment/ChangeStatus"
    mark_paid_data = {
        "Comment": "test deposit for rake testing",
        "PaymentRequestId": payment_request_id,
        "ChangeStatusTo": "MarkAsPaid",
        "ProcessingType": 0,
        "Type": "Deposit"
    }
    
    # Use PATCH method? Let's try POST first
    resp2 = requests.patch(mark_paid_url, headers=headers, json=mark_paid_data)
    if resp2.status_code != 200:
        print(f"MarkAsPaid failed: {resp2.status_code} - {resp2.text}")
        # Maybe it's POST? Try POST
        resp2 = requests.post(mark_paid_url, headers=headers, json=mark_paid_data)
        if resp2.status_code != 200:
            print(f"MarkAsPaid POST also failed: {resp2.status_code} - {resp2.text}")
            return False
    
    print("✅ Deposit marked as paid")
    
    # 3. Verify balance via Wallet API
    wallet_url = f"https://wallet.qa.sofon.one/5/api/v1/balance/{player_id}/USD"
    resp3 = requests.get(wallet_url)
    if resp3.status_code == 200:
        balance_data = resp3.json()
        print(f"Wallet balance after deposit: {json.dumps(balance_data, indent=2)}")
    else:
        print(f"Wallet check failed: {resp3.status_code}")
    
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python temp_deposit.py <playerId>")
        sys.exit(1)
    player_id = int(sys.argv[1])
    make_deposit(player_id)