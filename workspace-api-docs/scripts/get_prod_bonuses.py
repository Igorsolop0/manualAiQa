#!/usr/bin/env python3
"""
Get bonuses from PROD and analyze BetRealPercent
Goal: Find bonuses that wager from bonus balance (BetRealPercent = 0 or low)
"""

import requests
import json
from datetime import datetime

# PROD Configuration
BACKOFFICE_API_URL = "https://adminwebapi.prod.sofon.one/api"
BACKOFFICE_USER_ID = 560  # Prod default
PARTNER_ID = 5  # MineBit

# Headers for BackOffice API
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "UserId": str(BACKOFFICE_USER_ID)
}

def get_bonuses():
    """Get all bonuses from PROD"""
    print("\n" + "=" * 60)
    print("GET BONUSES FROM PROD")
    print("=" * 60)

    url = f"{BACKOFFICE_API_URL}/Bonus/GetBonuses"

    payload = {
        "partnerId": PARTNER_ID,
        "takeCount": 100,  # Get up to 100 bonuses
        "skipCount": 0,
        "isActive": True  # Only active bonuses
    }

    print(f"\nURL: {url}")
    print(f"UserId header: {BACKOFFICE_USER_ID}")
    print(f"Request: partnerId={PARTNER_ID}, takeCount=100, isActive=True")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"\nStatus: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return None

        result = response.json()
        print(f"ResponseCode: {result.get('ResponseCode')}")
        print(f"Description: {result.get('Description')}")

        if result.get("ResponseCode") != "Success":
            print(f"❌ API returned non-success: {result}")
            return None

        bonuses = result.get("ResponseObject", [])
        print(f"\n✅ Retrieved {len(bonuses)} bonuses")

        return bonuses

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def analyze_bonuses(bonuses):
    """Analyze bonuses by BetRealPercent"""
    print("\n" + "=" * 60)
    print("BONUS ANALYSIS - BetRealPercent")
    print("=" * 60)

    welcome_bonuses = []
    bonus_balance_wagers = []  # BetRealPercent = 0
    real_balance_wagers = []  # BetRealPercent > 0
    promocode_bonuses = []
    unknown_bet_real = []

    for bonus in bonuses:
        if not isinstance(bonus, dict):
            continue

        bonus_name = bonus.get("Name", "Unknown")
        bonus_id = bonus.get("Id", 0)
        trigger = bonus.get("TriggerType", "Unknown")
        bet_real_percent = bonus.get("BetRealPercent", "Unknown")
        is_active = bonus.get("IsActive", False)

        # Categorize by BetRealPercent
        if bet_real_percent == 100:
            welcome_bonuses.append({
                "id": bonus_id,
                "name": bonus_name,
                "trigger": trigger,
                "bet_real_percent": bet_real_percent,
                "active": is_active
            })
            print(f"🟢 Welcome Bonus: {bonus_name} (ID: {bonus_id}, BetRealPercent: {bet_real_percent})")

        elif bet_real_percent == 0:
            bonus_balance_wagers.append({
                "id": bonus_id,
                "name": bonus_name,
                "trigger": trigger,
                "bet_real_percent": bet_real_percent,
                "active": is_active
            })
            print(f"🔴 Bonus Balance: {bonus_name} (ID: {bonus_id}, BetRealPercent: {bet_real_percent})")

        elif bet_real_percent > 0 and bet_real_percent < 50:
            bonus_balance_wagers.append({
                "id": bonus_id,
                "name": bonus_name,
                "trigger": trigger,
                "bet_real_percent": bet_real_percent,
                "active": is_active
            })
            print(f"🟡 Low Real %: {bonus_name} (ID: {bonus_id}, BetRealPercent: {bet_real_percent})")

        else:
            real_balance_wagers.append({
                "id": bonus_id,
                "name": bonus_name,
                "trigger": trigger,
                "bet_real_percent": bet_real_percent,
                "active": is_active
            })

        # Check for promocode trigger
        if isinstance(trigger, str) and "promocode" in trigger.lower():
            promocode_bonuses.append({
                "id": bonus_id,
                "name": bonus_name,
                "trigger": trigger,
                "bet_real_percent": bet_real_percent
            })

    return {
        "welcome_bonuses": welcome_bonuses,
        "bonus_balance_wagers": bonus_balance_wagers,
        "real_balance_wagers": real_balance_wagers,
        "promocode_bonuses": promocode_bonuses
    }

def main():
    print("=" * 60)
    print("BONUS BALANCE TYPES ANALYSIS - PROD")
    print("Environment: PROD")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    # Get bonuses
    bonuses = get_bonuses()
    if not bonuses:
        print("\n❌ Failed to retrieve bonuses")
        return

    # Analyze
    analysis = analyze_bonuses(bonuses)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"\nTotal Active Bonuses: {len(bonuses)}")
    print(f"🟢 Welcome Bonuses (BetRealPercent: 100%): {len(analysis['welcome_bonuses'])}")
    print(f"🔴 Bonus Balance Wagers (BetRealPercent: 0%): {len(analysis['bonus_balance_wagers'])}")
    print(f"🟡 Low Real % Bonuses (BetRealPercent: 0-50%): {len(analysis['bonus_balance_wagers'])}")
    print(f"🟢 Real Balance Wagers (BetRealPercent: >50%): {len(analysis['real_balance_wagers'])}")
    print(f"🎫 Promo Code Bonuses: {len(analysis['promocode_bonuses'])}")

    # Detailed listings
    if analysis['welcome_bonuses']:
        print("\n🟢 Welcome Bonuses:")
        for bonus in analysis['welcome_bonuses']:
            print(f"   - ID {bonus['id']}: {bonus['name']} (Trigger: {bonus['trigger']})")

    if analysis['bonus_balance_wagers']:
        print("\n🔴 Bonus Balance Wagers (BetRealPercent = 0):")
        for bonus in analysis['bonus_balance_wagers']:
            print(f"   - ID {bonus['id']}: {bonus['name']} (Trigger: {bonus['trigger']})")

    if analysis['bonus_balance_wagers']:
        print("\n🟡 Low Real % Bonuses:")
        for bonus in analysis['bonus_balance_wagers']:
            print(f"   - ID {bonus['id']}: {bonus['name']} (BetRealPercent: {bonus['bet_real_percent']})")

    if analysis['promocode_bonuses']:
        print("\n🎫 Promo Code Bonuses:")
        for bonus in analysis['promocode_bonuses']:
            print(f"   - ID {bonus['id']}: {bonus['name']} (Trigger: {bonus['trigger']})")

    # Comparison with Welcome Bonus
    print("\n" + "=" * 60)
    print("COMPARISON: Welcome Bonus vs Bonus Balance Wagers")
    print("=" * 60)

    welcome_count = len(analysis['welcome_bonuses'])
    bonus_balance_count = len(analysis['bonus_balance_wagers'])

    print(f"\nWelcome Bonuses (BetRealPercent: 100%): {welcome_count}")
    print(f"Bonus Balance Wagers (BetRealPercent = 0%): {bonus_balance_count}")

    if welcome_count > 0 and bonus_balance_count > 0:
        print(f"\n✅ Found both types in system!")
        print(f"   - {welcome_count} bonuses wager from REAL balance (100%)")
        print(f"   - {bonus_balance_count} bonuses wager from BONUS balance (0%)")
    elif welcome_count > 0:
        print(f"\n⚠️ Only Welcome Bonus type found")
        print(f"   No bonuses wager from bonus balance")
    elif bonus_balance_count > 0:
        print(f"\n⚠️ Only Bonus Balance type found")
        print(f"   {bonus_balance_count} bonuses wager from bonus balance (0%)")
        print(f"   No Welcome Bonus type (100%) found")

    # Save results
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/bonus-balance-types"
    import os
    os.makedirs(output_dir, exist_ok=True)

    results = {
        "environment": "PROD",
        "timestamp": datetime.now().isoformat(),
        "total_bonuses": len(bonuses),
        "analysis": analysis,
        "summary": {
            "welcome_bonuses_count": len(analysis['welcome_bonuses']),
            "bonus_balance_wagers_count": len(analysis['bonus_balance_wagers']),
            "real_balance_wagers_count": len(analysis['real_balance_wagers']),
            "promocode_bonuses_count": len(analysis['promocode_bonuses'])
        },
        "all_bonuses": bonuses
    }

    output_file = f"{output_dir}/bonuses-prod-analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
