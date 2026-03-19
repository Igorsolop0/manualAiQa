#!/usr/bin/env python3
"""
Get bonus information for player via Website API and BackOffice API.
"""

import requests
import json
import sys

EMAIL = "demo1772613196064@nextcode.tech"
PASSWORD = "Qweasd123!"
PARTNER_ID = 5
BASE_URL_WEBSITE = "https://websitewebapi.qa.sofon.one"
BASE_URL_BACKOFFICE = "https://adminwebapi.qa.sofon.one"
USER_ID = 1  # QA environment
CLIENT_ID = 3563293

def login_website():
    """Login via Website API v3."""
    url = f"{BASE_URL_WEBSITE}/{PARTNER_ID}/api/v3/Client/Login"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60",
    }
    
    data = {
        "partnerId": PARTNER_ID,
        "email": EMAIL,
        "password": PASSWORD,
        "deviceType": 1,  # Desktop
    }
    
    print(f"🔐 Logging in {EMAIL}...")
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Response text: {response.text}")
        return None
    
    result = response.json()
    print(f"Login response: {json.dumps(result, indent=2)}")
    
    if result.get("ResponseCode") == "Success":
        token = result.get("ResponseObject", {}).get("Token")
        if token:
            print(f"✅ Login successful. Token: {token[:30]}...")
            return token
        else:
            print("❌ No token in response")
    else:
        print(f"❌ Login failed: {result.get('Description')}")
    
    return None

def get_bonuses_website(token):
    """Get bonuses via Website API."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60",
        "Authorization": token,  # Try both Authorization header
    }
    
    endpoints = [
        ("Active Bonuses", f"{BASE_URL_WEBSITE}/{PARTNER_ID}/api/v3/Bonus/GetActiveBonuses"),
        ("Available Bonuses", f"{BASE_URL_WEBSITE}/{PARTNER_ID}/api/v3/Bonus/GetBonuses"),
        ("Eligible Bonuses", f"{BASE_URL_WEBSITE}/{PARTNER_ID}/api/v3/Bonus/GetEligibleBonuses"),
        ("Promotions", f"{BASE_URL_WEBSITE}/{PARTNER_ID}/api/v3/Bonus/GetPromotions"),
        ("Available Deposit Bonuses", f"{BASE_URL_WEBSITE}/{PARTNER_ID}/api/v3/Bonus/GetAvailableDepositBonuses"),
    ]
    
    results = {}
    
    for name, url in endpoints:
        print(f"\n🎁 Getting {name}...")
        try:
            # Try with empty body first
            response = requests.post(url, json={}, headers=headers)
            if response.status_code == 200:
                data = response.json()
                results[name] = data
                print(f"✅ {name}: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ {name} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ {name} error: {e}")
    
    return results

def get_client_bonuses_backoffice():
    """Get client bonuses via BackOffice API."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "UserId": str(USER_ID),
    }
    
    # Try to find bonus-related endpoints
    endpoints = [
        ("Client Details", f"{BASE_URL_BACKOFFICE}/api/Client/GetClientById"),
        ("Client Bonuses", f"{BASE_URL_BACKOFFICE}/api/Bonus/GetClientBonuses"),
        ("Active Bonuses", f"{BASE_URL_BACKOFFICE}/api/Bonus/GetActiveBonuses"),
        ("Bonus History", f"{BASE_URL_BACKOFFICE}/api/Bonus/GetBonusHistory"),
    ]
    
    results = {}
    
    for name, url in endpoints:
        print(f"\n🏢 BackOffice: Getting {name}...")
        try:
            data = {"clientId": CLIENT_ID}
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                results[name] = data
                print(f"✅ {name}: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ {name} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ {name} error: {e}")
    
    return results

def get_wallet_balance():
    """Get balance via Wallet API."""
    url = f"https://wallet.qa.sofon.one/{PARTNER_ID}/api/v1/balance/{CLIENT_ID}/USD"
    
    print(f"\n💰 Wallet balance...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Balance: {json.dumps(data, indent=2)}")
            return data
        else:
            print(f"❌ Balance failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Balance error: {e}")
    
    return None

def main():
    print("🔍 Checking bonus information for player...")
    print(f"Email: {EMAIL}")
    print(f"Client ID: {CLIENT_ID}")
    
    # Try Website API login first
    token = login_website()
    
    if token:
        # Get bonuses via Website API
        website_results = get_bonuses_website(token)
    else:
        print("\n⚠️  Website login failed, trying BackOffice API...")
        website_results = {}
    
    # Get client info via BackOffice API
    backoffice_results = get_client_bonuses_backoffice()
    
    # Get wallet balance
    balance = get_wallet_balance()
    
    # Summary
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    
    if token:
        print(f"✅ Website login successful")
    else:
        print(f"❌ Website login failed")
    
    print(f"\n🏢 BackOffice results: {len(backoffice_results)} endpoints responded")
    
    if balance:
        print(f"\n💰 Wallet balance: ${balance.get('AvailableMain', 0):.2f}")
    
    # Check for rakeback specifically
    print("\n🔍 Looking for Realtime Rakeback (rakeback) data...")
    
    all_data = {**website_results, **backoffice_results}
    for name, data in all_data.items():
        if isinstance(data, dict):
            data_str = json.dumps(data).lower()
            if 'rake' in data_str or 'rakeback' in data_str or 'real-time' in data_str:
                print(f"\n🎯 Found possible rakeback in {name}:")
                print(json.dumps(data, indent=2))
                break

if __name__ == "__main__":
    main()