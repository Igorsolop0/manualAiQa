import json
import requests
import random
import string

def credit_player(player_id):
    """
    Add money to player via Wallet API debit correction
    """
    base_url = "https://wallet.qa.sofon.one"
    partner_id = 5
    currency = "USD"
    amount = 100.0
    
    # Generate external transaction ID
    external_tx_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    
    endpoint = f"{base_url}/{partner_id}/api/v1/transaction/correction/debit"
    
    data = {
        "clientId": player_id,
        "currency": currency,
        "amount": amount,
        "externalTransactionId": external_tx_id,
        "comment": "Credit for rake testing"
    }
    
    print(f"Crediting {amount} {currency} to player {player_id}...")
    resp = requests.post(endpoint, json=data)
    
    if resp.status_code != 200:
        print(f"Credit failed: {resp.status_code} - {resp.text}")
        return False
    
    result = resp.json()
    print(f"Credit response: {json.dumps(result, indent=2)}")
    
    # Verify balance
    balance_url = f"{base_url}/{partner_id}/api/v1/balance/{player_id}/{currency}"
    resp2 = requests.get(balance_url)
    if resp2.status_code == 200:
        balance = resp2.json()
        print(f"Updated balance: {json.dumps(balance, indent=2)}")
    else:
        print(f"Balance check failed: {resp2.status_code}")
    
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python temp_credit.py <playerId>")
        sys.exit(1)
    player_id = int(sys.argv[1])
    credit_player(player_id)