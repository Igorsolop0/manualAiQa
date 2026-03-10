import os
import sys
import json
import uuid
import urllib.request
import urllib.error
import argparse
from urllib.parse import urlparse

def register_user(env, out_file):
    domain = 'minebit-casino.dev.sofon.one' if env == 'dev' else f'minebit-casino.{env}.sofon.one'
    url = f"https://{domain}/graphql"
    
    # Generate unique test user data
    unique_id = str(uuid.uuid4().hex)[:8]
    email = f"testqa_{unique_id}@mail.com"
    password = "Password123!"
    
    print(f"[*] Registering new user {email} on {domain}...")

    variables = {
        "bmsPartnerId": 5,
        "locale": "en",
        "deviceFingerPrint": "bafe3c5f7c6fff4fb2c46c2a1a250ebf",
        "fraudCheckDeviceFingerPrint": None,
        "input": {
            "email": email,
            "password": password,
            "currency": "USD",
            "promoCode": None,
            "termsConditionsAccepted": True,
            "affiliateData": f"https://{domain}/"
        }
    }

    payload = {
        "operationName": "PlayerRegisterUniversal",
        "variables": variables,
        "query": """
        mutation PlayerRegisterUniversal($bmsPartnerId: Int!, $input: PlayerRegisterUniversalInput!, $locale: Locale!, $deviceFingerPrint: String, $fraudCheckDeviceFingerPrint: String) {
          playerRegisterUniversal(
            bmsPartnerId: $bmsPartnerId
            input: $input
            locale: $locale
            deviceFingerPrint: $deviceFingerPrint
            fraudCheckDeviceFingerPrint: $fraudCheckDeviceFingerPrint
          ) {
            problems {
              message
              problemCode
              traceId
              __typename
            }
            record {
              sessionToken
              userName
              id
              email
              __typename
            }
            status
            __typename
          }
        }
        """
    }
    
    headers = {
        "Content-Type": "application/json",
        "authorization": "",
        "website-locale": "en",
        "website-origin": f"https://{domain}"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            data = json.loads(response_data)
        
        if "errors" in data:
            print("[!] GraphQL Errors:", json.dumps(data["errors"], indent=2))
            sys.exit(1)
            
        result = data.get("data", {}).get("playerRegisterUniversal", {})
        if result.get("status") != "SUCCESS":
            print("[!] Registration failed:", json.dumps(result.get("problems"), indent=2))
            sys.exit(1)
            
        record = result.get("record", {})
        session_token = record.get("sessionToken")
        client_id = record.get("id")
        user_name = record.get("userName")
        
        print(f"[+] Successfully registered user: {email} (ID: {client_id})")
        
        # Save to credential store
        credential_data = {
            "environment": env,
            "domain": domain,
            "email": email,
            "password": password,
            "userName": user_name,
            "clientId": client_id,
            "sessionToken": session_token
        }
        
        with open(out_file, 'w') as f:
            json.dump(credential_data, f, indent=2)
            
        print(f"[+] Credentials saved to: {out_file}")
        
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"[!] HTTP Error {e.code}: {e.reason}")
        print(f"Body: {body}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error making request: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a test player for automated testing")
    parser.add_argument("--env", required=True, choices=["dev", "qa", "stage", "prod"], help="Target environment")
    parser.add_argument("--out", required=True, help="Path to save the credentials JSON file")
    
    args = parser.parse_args()
    register_user(args.env, args.out)
