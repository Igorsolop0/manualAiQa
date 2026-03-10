import json
import requests
import time
import sys

def register_player():
    url = "https://minebit-casino.qa.sofon.one/graphql"
    timestamp = int(time.time() * 1000)
    import random
    random_suffix = random.randint(1000, 9999)
    email = f"test-rakecheck-{timestamp}-{random_suffix}@nextcode.tech"
    password = "Qweasd123!"
    
    mutation = """
    mutation PlayerRegisterUniversal(
        $input: PlayerRegisterUniversalInput!
        $bmsPartnerId: Int!
        $locale: Locale!
        $deviceFingerPrint: String
    ) {
        playerRegisterUniversal(
            input: $input
            bmsPartnerId: $bmsPartnerId
            locale: $locale
            deviceFingerPrint: $deviceFingerPrint
        ) {
            record {
                sessionToken
                userName
                id
                email
            }
            status
        }
    }
    """
    
    variables = {
        "input": {
            "email": email,
            "password": password,
            "currency": "USD",
            "promoCode": None,
            "termsConditionsAccepted": True,
            "affiliateData": "https://minebit-casino.qa.sofon.one",
        },
        "bmsPartnerId": 5,
        "locale": "en",
        "deviceFingerPrint": "".join([str(random.randint(0, 9)) for _ in range(32)])
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://minebit-casino.qa.sofon.one",
        "Referer": "https://minebit-casino.qa.sofon.one/",
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60",
    }
    
    payload = {
        "operationName": "PlayerRegisterUniversal",
        "variables": variables,
        "query": mutation
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"HTTP error: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    if "errors" in data:
        print(f"GraphQL errors: {data['errors']}")
        return None
    
    record = data.get("data", {}).get("playerRegisterUniversal", {}).get("record")
    if not record:
        print(f"No record returned: {data}")
        return None
    
    print(f"✅ Player registered: {email}")
    print(f"Session token: {record.get('sessionToken')}")
    print(f"Player ID: {record.get('id')}")
    return record

if __name__ == "__main__":
    result = register_player()
    if result:
        sys.stdout.write(json.dumps(result))