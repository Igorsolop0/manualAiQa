import json
import requests
import random
import string

def credit_via_backoffice(player_id):
    base_url = "https://adminwebapi.qa.sofon.one"
    headers = {
        "Content-Type": "application/json",
        "UserId": "1",
    }
    
    endpoint = f"{base_url}/api/Client/CreateDebitCorrection"
    
    # Generate unique external ID
    external_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    
    data = {
        "clientId": player_id,
        "amount": 100.0,
        "currency": "USD",
        "externalTransactionId": external_id,
        "comment": "Credit for rake testing",
        "isTest": True
    }
    
    print(f"Creating debit correction for player {player_id}...")
    resp = requests.post(endpoint, headers=headers, json=data)
    
    if resp.status_code != 200:
        print(f"Request failed: {resp.status_code} - {resp.text}")
        return False
    
    result = resp.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Verify balance via Wallet API
    wallet_url = f"https://wallet.qa.sofon.one/5/api/v1/balance/{player_id}/USD"
    resp2 = requests.get(wallet_url)
    if resp2.status_code == 200:
        balance = resp2.json()
        print(f"Updated balance: {json.dumps(balance, indent=2)}")
    else:
        print(f"Balance check failed: {resp2.status_code}")
    
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python temp_bo_credit.py <playerId>")
        sys.exit(1)
    player_id = int(sys.argv[1])
    credit_via_backoffice(player_id)