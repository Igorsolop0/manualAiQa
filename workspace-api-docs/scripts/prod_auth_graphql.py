#!/usr/bin/env python3
"""
Register and authenticate player on PROD via GraphQL API for CT-476 testing.
This bypasses the broken Login endpoint by creating a new test account.
"""

import json
import sys
import argparse
import subprocess
from datetime import datetime
import random

try:
    import requests
except ImportError:
    requests = None

PARTNER_ID = 5
GRAPHQL_URL = "https://minebit-casino.prod.sofon.one/graphql"
WEBSITE_URL = "https://minebit-casino.prod.sofon.one"


def mask_secret(value):
    if not value:
        return "<empty>"
    if len(value) <= 10:
        return "***"
    return f"{value[:6]}...{value[-4:]}"


def generate_fingerprint():
    """Generate random device fingerprint."""
    return ''.join([str(random.randint(0, 9)) for _ in range(32)])

def register_player_via_graphql():
    """Register new player via GraphQL mutation and get session token."""
    if requests is None:
        raise RuntimeError("Missing dependency: requests. Install with `pip install requests`.")
    
    timestamp = int(datetime.now().timestamp() * 1000)
    random_suffix = random.randint(1000, 9999)
    email = f"ct476-test-{timestamp}-{random_suffix}@nextcode.tech"
    password = "TestPass123!"
    fingerprint = generate_fingerprint()
    
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
            "affiliateData": WEBSITE_URL,
        },
        "bmsPartnerId": PARTNER_ID,
        "locale": "en",
        "deviceFingerPrint": fingerprint,
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": WEBSITE_URL,
        "Referer": f"{WEBSITE_URL}/",
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60",
    }
    
    payload = {
        "operationName": "PlayerRegisterUniversal",
        "variables": variables,
        "query": mutation
    }
    
    print(f"🔐 Registering new player on PROD via GraphQL...")
    print(f"Email: {email}")
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        result = response.json()
        
        # Check for GraphQL errors
        if "errors" in result:
            print(f"\n❌ GraphQL errors:")
            print(json.dumps(result["errors"], indent=2, ensure_ascii=False))
            raise Exception("GraphQL registration failed")
        
        # Extract player data
        record = result.get("data", {}).get("playerRegisterUniversal", {}).get("record")
        
        if not record:
            print(f"\n❌ No record in response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            raise Exception("Registration failed: No record returned")
        
        player_data = {
            "id": record.get("id"),
            "email": record.get("email"),
            "userName": record.get("userName"),
            "sessionToken": record.get("sessionToken"),
            "password": password,
            "partnerId": PARTNER_ID,
            "environment": "prod",
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n✅ Registration successful!")
        print(f"Player ID: {player_data['id']}")
        print(f"Email: {player_data['email']}")
        print(f"Username: {player_data['userName']}")
        print(f"Session Token: {mask_secret(player_data['sessionToken'])}")
        
        return player_data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        raise

def test_token(session_token):
    """Test session token by making authenticated GraphQL query."""
    if requests is None:
        raise RuntimeError("Missing dependency: requests. Install with `pip install requests`.")
    
    query = """
    query GetPlayerProfile {
        player {
            id
            email
            userName
            balances {
                currencyId
                amount
            }
        }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": session_token,
        "website-locale": "en",
        "website-origin": WEBSITE_URL,
        "x-time-zone-offset": "-60",
    }
    
    payload = {
        "operationName": "GetPlayerProfile",
        "query": query,
        "variables": {}
    }
    
    print(f"\n🧪 Testing session token with profile query...")
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers, timeout=10)
        result = response.json()
        
        if "errors" in result:
            print(f"❌ Token validation failed:")
            print(json.dumps(result["errors"], indent=2, ensure_ascii=False))
            return False
        
        player = result.get("data", {}).get("player")
        if player:
            print(f"✅ Token is valid! Player profile retrieved.")
            print(f"   ID: {player.get('id')}")
            print(f"   Email: {player.get('email')}")
            print(f"   Balances: {len(player.get('balances', []))} currencies")
            return True
        else:
            print(f"⚠️ No player data in response")
            return False
            
    except Exception as e:
        print(f"❌ Token test failed: {e}")
        return False

def save_auth_data(auth_data):
    """Save auth data to workspace for Clawver."""
    import os
    
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-auth"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/prod-player-auth.json"
    
    with open(output_file, 'w') as f:
        json.dump(auth_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Auth data saved to: {output_file}")
    
    # Also create a simple token file for easy access
    token_file = f"{output_dir}/token.txt"
    with open(token_file, 'w') as f:
        f.write(auth_data['sessionToken'])
    
    print(f"\n📋 Usage for Clawver:")
    print("   Token saved to token.txt (masked output in logs)")
    print(f"   Option 1 - Authorization header: [use token file ref]")
    print(f"   Option 2 - Cookie: session_token=[use token file ref]")
    print(f"   ")
    print(f"   Option 3 - Set cookie in browser context:")
    print(f"   await context.addCookies([{{")
    print(f"     name: 'session_token',")
    print(f"     value: '<read from token_ref>',")
    print(f"     domain: 'minebit-casino.prod.sofon.one',")
    print(f"     path: '/'")
    print(f"   }}]);")
    
    return output_file, token_file


def register_session_record(run_id, ticket, storage_ref, token_ref):
    """Optional: register session-record in Phase 2 pilot registry."""
    cmd = [
        "python3",
        "/Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py",
        "register-session",
        "--project",
        "minebit",
        "--subject-type",
        "player",
        "--owner",
        "api-docs-agent",
        "--storage-state-ref",
        storage_ref,
        "--token-ref",
        token_ref,
        "--status",
        "active",
        "--refresh-strategy",
        "api_refresh",
    ]
    if run_id:
        cmd.extend(["--run-id", run_id])
    if ticket:
        cmd.extend(["--ticket", ticket])
    if not run_id and not ticket:
        return
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"⚠️ Session record registration failed: {exc}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PROD auth via GraphQL registration")
    parser.add_argument("--run-id", default=None, help="Optional Phase 2 run_id")
    parser.add_argument("--ticket", default=None, help="Optional ticket key (CT-XXX)")
    args = parser.parse_args()

    try:
        print("=" * 60)
        print("CT-476 PROD Authentication via GraphQL Registration")
        print("=" * 60)
        print()
        
        auth_data = register_player_via_graphql()
        
        if test_token(auth_data['sessionToken']):
            output_file, token_file = save_auth_data(auth_data)
            register_session_record(
                run_id=args.run_id,
                ticket=args.ticket,
                storage_ref="workspace/shared/test-auth/prod-player-auth.json",
                token_ref="workspace/shared/test-auth/token.txt",
            )
            print(f"\n✅ All done! Auth data ready for Clawver at:")
            print(f"   {output_file}")
            sys.exit(0)
        else:
            print(f"\n⚠️ Registration succeeded but token validation failed")
            save_auth_data(auth_data)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
