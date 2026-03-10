#!/usr/bin/env python3
"""
Check rakeback status using GraphQL queries from user.
"""

import requests
import json
import sys

GRAPHQL_URL = "https://minebit-casino.qa.sofon.one/graphql"
AUTH_TOKEN = "Bearer 19ce3e425ec44271a2099a92993cc9dd"
BONUS_ID = 2469229  # From user
PARTNER_ID = 5

headers = {
    "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,de;q=0.7",
    "Connection": "keep-alive",
    "Host": "minebit-casino.qa.sofon.one",
    "Origin": "https://minebit-casino.qa.sofon.one",
    "Referer": "https://minebit-casino.qa.sofon.one/bonuses-new",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "accept": "*/*",
    "authorization": AUTH_TOKEN,
    "content-type": "application/json",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "website-locale": "en",
    "website-origin": "https://minebit-casino.qa.sofon.one",
    "x-time-zone-offset": "-60",
}

def query_eligible_bonuses():
    """Query eligible bonuses (including rakeback)."""
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
    
    variables = {
        "bmsPartnerId": PARTNER_ID
    }
    
    payload = {
        "operationName": "EligibleBonuses",
        "variables": variables,
        "query": query
    }
    
    print("🎁 Querying eligible bonuses...")
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Query failed: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    # Look for rakeback bonus
    bonuses = data.get("data", {}).get("eligibleBonuses", [])
    print(f"\n📊 Found {len(bonuses)} eligible bonuses:")
    
    for bonus in bonuses:
        print(f"\n  ID: {bonus.get('id')}")
        print(f"  BMS Bonus ID: {bonus.get('bmsBonusId')}")
        print(f"  Amount: ${bonus.get('amount', 0):.2f}")
        print(f"  isAvailable: {bonus.get('isAvailable')}")
        print(f"  isPendingCalculation: {bonus.get('isPendingCalculation')}")
        print(f"  nextAvailableAt: {bonus.get('nextAvailableAt')}")
        print(f"  previousAvailableAt: {bonus.get('previousAvailableAt')}")
        print(f"  lastClaimedAt: {bonus.get('lastClaimedAt')}")
        print(f"  hasWagering: {bonus.get('hasWagering')}")
        
        # Check if this is the rakeback bonus (ID 2469229)
        if bonus.get('bmsBonusId') == BONUS_ID:
            print("  🎯 THIS IS THE RAKEBACK BONUS!")
            return bonus
    
    return None

def query_bonus_details(bonus_id):
    """Query details for specific bonus."""
    query = """
    query BonusDetails($bmsPartnerId: Int!, $bonusId: Int) {
      bonusDetails(bmsPartnerId: $bmsPartnerId, bonusId: $bonusId) {
        id
        name
        validTill
        availableInProducts
        turnOverCount
        __typename
      }
    }
    """
    
    variables = {
        "bmsPartnerId": PARTNER_ID,
        "bonusId": bonus_id
    }
    
    payload = {
        "operationName": "BonusDetails",
        "variables": variables,
        "query": query
    }
    
    print(f"\n📋 Querying bonus details for ID {bonus_id}...")
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Query failed: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    return data.get("data", {}).get("bonusDetails")

def check_wallet_balance():
    """Check wallet balance for player 3563293."""
    url = f"https://wallet.qa.sofon.one/{PARTNER_ID}/api/v1/balance/3563293/USD"
    
    print(f"\n💰 Checking wallet balance...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Balance check failed: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    print(f"Balance: {json.dumps(data, indent=2)}")
    return data

def main():
    print("🔍 Checking Realtime Rakeback status...")
    print(f"Bonus ID: {BONUS_ID}")
    print(f"Auth token: {AUTH_TOKEN[:30]}...")
    
    try:
        # Check eligible bonuses
        rakeback_bonus = query_eligible_bonuses()
        
        if rakeback_bonus:
            print(f"\n🎯 Realtime Rakeback Status:")
            print(f"   Bonus ID: {rakeback_bonus.get('bmsBonusId')}")
            print(f"   Amount: ${rakeback_bonus.get('amount', 0):.2f}")
            print(f"   Available: {rakeback_bonus.get('isAvailable')}")
            print(f"   Pending Calculation: {rakeback_bonus.get('isPendingCalculation')}")
            print(f"   Next Available At: {rakeback_bonus.get('nextAvailableAt')}")
            
            # Check amount - should be $0.25 for $100 wager
            amount = rakeback_bonus.get('amount', 0)
            if amount > 0:
                print(f"   ✅ Rakeback amount calculated: ${amount:.2f}")
                if amount == 0.25:
                    print(f"   ✅ CORRECT: $0.25 for $100 wager (0.25% House Edge × 10%)")
                else:
                    print(f"   ⚠️  UNEXPECTED: Expected $0.25, got ${amount:.2f}")
            else:
                print(f"   ⏳ Amount not calculated yet (isPendingCalculation: {rakeback_bonus.get('isPendingCalculation')})")
            
            # Check timing
            next_available = rakeback_bonus.get('nextAvailableAt')
            if next_available:
                print(f"   ⏰ Next claim available at: {next_available}")
        
        # Get bonus details
        bonus_details = query_bonus_details(BONUS_ID)
        if bonus_details:
            print(f"\n📋 Bonus Details:")
            print(f"   Name: {bonus_details.get('name')}")
            print(f"   Valid Till: {bonus_details.get('validTill')}")
            print(f"   Turnover Count: {bonus_details.get('turnOverCount')}")
        
        # Check wallet balance
        balance = check_wallet_balance()
        if balance:
            print(f"\n💵 Current Balance:")
            print(f"   Available Main: ${balance.get('AvailableMain', 0):.2f}")
            print(f"   Available Bonus: ${balance.get('AvailableBonus', 0):.2f}")
            print(f"   Used: ${balance.get('Balances', {}).get('Used', 0):.2f}")
        
        # Summary
        print("\n" + "="*50)
        print("📋 RAKEBACK TEST SUMMARY")
        print("="*50)
        
        if rakeback_bonus:
            if rakeback_bonus.get('isAvailable'):
                print("✅ Rakeback bonus is AVAILABLE for claim!")
                print(f"   Amount: ${rakeback_bonus.get('amount', 0):.2f}")
                print("   Next step: Click 'Claim' button in UI")
            elif rakeback_bonus.get('isPendingCalculation'):
                print("⏳ Rakeback bonus is PENDING CALCULATION")
                print("   Wait a bit longer (batch processing every 30min)")
            else:
                print("❓ Rakeback status unclear")
                print(f"   isAvailable: {rakeback_bonus.get('isAvailable')}")
                print(f"   isPendingCalculation: {rakeback_bonus.get('isPendingCalculation')}")
        else:
            print("❌ Rakeback bonus not found in eligible bonuses")
            print("   Possible issues:")
            print("   1. 30-minute batch hasn't run yet")
            print("   2. Player is in test segment")
            print("   3. Bonus campaign not active")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()