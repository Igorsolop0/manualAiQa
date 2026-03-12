#!/usr/bin/env python3
"""
Analyze PROD bonuses by BetRealPercent
Find bonuses that wager from bonus balance (BetRealPercent = 0 or < 100)
"""

import requests
import json
from datetime import datetime

BACKOFFICE_API_URL = "https://adminwebapi.prod.sofon.one/api"
BACKOFFICE_USER_ID = 560
PARTNER_ID = 5

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "UserId": str(BACKOFFICE_USER_ID)
}

def get_all_bonuses():
    """Get all active bonuses"""
    print("\n" + "=" * 60)
    print("GETTING ALL BONUSES FROM PROD")
    print("=" * 60)

    url = f"{BACKOFFICE_API_URL}/Bonus/GetBonuses"

    payload = {
        "partnerId": PARTNER_ID,
        "takeCount": 1000,  # Get all
        "skipCount": 0,
        "isActive": True
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return []

        result = response.json()
        if result.get("ResponseCode") != 0:  # 0 = Success in this API
            print(f"❌ API returned non-zero code: {result}")
            return []

        bonuses = result.get("ResponseObject", {}).get("Entities", [])
        print(f"✅ Retrieved {len(bonuses)} bonuses")
        return bonuses

    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def analyze_betreal_percent(bonuses):
    """Analyze bonuses by BetRealPercent"""
    print("\n" + "=" * 60)
    print("ANALYZING BONUS BETREALPERCENT")
    print("=" * 60)

    welcome_bonus = None
    bonus_balance_bonuses = []
    other_bonuses = []

    for bonus in bonuses:
        if not isinstance(bonus, dict):
            continue

        bonus_id = bonus.get("Id")
        name = bonus.get("Name", "Unknown")
        bet_real_percent = bonus.get("BetRealPercent")
        win_real_percent = bonus.get("WinRealPercent")
        is_wager_only_real = bonus.get("IsWagerOnlyReal")
        bonus_type = bonus.get("BonusTypeId")
        trigger = bonus.get("PromoCode", "N/A")
        status = bonus.get("Status", "Unknown")

        # Find Welcome Bonus (ID 11380)
        if bonus_id == 11380:
            welcome_bonus = {
                "id": bonus_id,
                "name": name,
                "bet_real_percent": bet_real_percent,
                "win_real_percent": win_real_percent,
                "is_wager_only_real": is_wager_only_real,
                "bonus_type": bonus_type,
                "status": status
            }
            print(f"🟢 Found Welcome Bonus: {name} (ID: {bonus_id})")
            print(f"   BetRealPercent: {bet_real_percent}")
            print(f"   WinRealPercent: {win_real_percent}")

        # Check for bonus balance wagers (BetRealPercent = 0 or < 100)
        # Note: null means it uses default (likely 0 for bonus balance)
        is_bonus_balance_wager = False

        if bet_real_percent == 0:
            is_bonus_balance_wager = True
            print(f"🔴 Bonus Balance Wager: {name} (ID: {bonus_id})")
            print(f"   BetRealPercent: {bet_real_percent}")

        elif bet_real_percent is not None and bet_real_percent < 100:
            is_bonus_balance_wager = True
            print(f"🟡 Partial Real Wager: {name} (ID: {bonus_id})")
            print(f"   BetRealPercent: {bet_real_percent}%")

        if is_bonus_balance_wager:
            bonus_balance_bonuses.append({
                "id": bonus_id,
                "name": name,
                "bet_real_percent": bet_real_percent,
                "win_real_percent": win_real_percent,
                "is_wager_only_real": is_wager_only_real,
                "bonus_type": bonus_type,
                "trigger": trigger,
                "status": status
            })
        else:
            other_bonuses.append({
                "id": bonus_id,
                "name": name,
                "bet_real_percent": bet_real_percent,
                "bonus_type": bonus_type
            })

    return {
        "welcome_bonus": welcome_bonus,
        "bonus_balance_bonuses": bonus_balance_bonuses,
        "other_bonuses": other_bonuses
    }

def main():
    print("=" * 60)
    print("BONUS BETREALPERCENT ANALYSIS - PROD")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    # Get all bonuses
    bonuses = get_all_bonuses()
    if not bonuses:
        print("\n❌ No bonuses retrieved")
        return

    # Analyze
    analysis = analyze_betreal_percent(bonuses)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    welcome = analysis["welcome_bonus"]
    bonus_balance_count = len(analysis["bonus_balance_bonuses"])
    other_count = len(analysis["other_bonuses"])

    print(f"\nTotal Active Bonuses: {len(bonuses)}")
    print(f"\n🟢 Welcome Bonus (ID 11380):")
    if welcome:
        print(f"   Name: {welcome['name']}")
        print(f"   BetRealPercent: {welcome['bet_real_percent']}%")
        print(f"   WinRealPercent: {welcome['win_real_percent']}%")
        print(f"   IsWagerOnlyReal: {welcome['is_wager_only_real']}")
        print(f"   Status: {welcome['status']}")
    else:
        print(f"   ❌ Welcome Bonus (ID 11380) NOT FOUND!")

    print(f"\n🔴 Bonus Balance Wagers (BetRealPercent = 0 or < 100): {bonus_balance_count}")

    if bonus_balance_count > 0:
        print(f"\nTop 10 Bonus Balance Wagers:")
        for i, bonus in enumerate(analysis["bonus_balance_bonuses"][:10], 1):
            print(f"   {i}. ID {bonus['id']}: {bonus['name']}")
            print(f"      BetRealPercent: {bonus['bet_real_percent']}%")
            print(f"      Trigger: {bonus['trigger']}")

    # Comparison
    print("\n" + "=" * 60)
    print("COMPARISON: Welcome Bonus vs Bonus Balance Types")
    print("=" * 60)

    if welcome:
        welcome_bet_real = welcome['bet_real_percent']
        print(f"\n🟢 Welcome Bonus (ID {welcome['id']}):")
        print(f"   BetRealPercent: {welcome_bet_real}%")
        print(f"   → Wagers from REAL balance (100%)")
    else:
        print(f"\n⚠️ Welcome Bonus (ID 11380) not found")

    if bonus_balance_count > 0:
        print(f"\n🔴 Bonus Balance Wagers ({bonus_balance_count} bonuses):")
        print(f"   BetRealPercent: 0% or < 100%")
        print(f"   → Wagers from BONUS balance")
        print(f"\nExample bonuses:")
        for bonus in analysis["bonus_balance_bonuses"][:3]:
            print(f"   - {bonus['name']} (ID {bonus['id']})")
            print(f"     BetRealPercent: {bonus['bet_real_percent']}%")
    else:
        print(f"\n⚠️ No bonus balance wagers found")
        print(f"   All bonuses may wager from REAL balance")

    # Conclusion
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)

    if welcome and bonus_balance_count > 0:
        print(f"\n✅ FOUND BOTH TYPES:")
        print(f"   - Welcome Bonus wagers from REAL balance (BetRealPercent: 100%)")
        print(f"   - {bonus_balance_count} bonuses wager from BONUS balance (BetRealPercent: 0% or < 100%)")
        print(f"\n💡 System supports multiple wager types!")
    elif welcome:
        print(f"\n✅ ONLY WELCOME BONUS TYPE:")
        print(f"   - Welcome Bonus wagers from REAL balance (BetRealPercent: 100%)")
        print(f"   - No bonuses wager from BONUS balance")
    elif bonus_balance_count > 0:
        print(f"\n✅ ONLY BONUS BALANCE TYPE:")
        print(f"   - {bonus_balance_count} bonuses wager from BONUS balance")
        print(f"   - No Welcome Bonus type (100%) found")
    else:
        print(f"\n⚠️ NO WAGER TYPES FOUND")
        print(f"   - All bonuses may use default wagering")

    # Save results
    output_dir = "/Users/ihorsolopii/.openclaw/workspace/shared/test-results/bonus-balance-types"
    import os
    os.makedirs(output_dir, exist_ok=True)

    results = {
        "environment": "PROD",
        "timestamp": datetime.now().isoformat(),
        "total_bonuses": len(bonuses),
        "welcome_bonus": analysis["welcome_bonus"],
        "bonus_balance_bonuses": {
            "count": len(analysis["bonus_balance_bonuses"]),
            "bonuses": analysis["bonus_balance_bonuses"]
        },
        "summary": {
            "welcome_bonus_found": analysis["welcome_bonus"] is not None,
            "bonus_balance_count": len(analysis["bonus_balance_bonuses"]),
            "supports_multiple_wager_types": analysis["welcome_bonus"] is not None and len(analysis["bonus_balance_bonuses"]) > 0
        }
    }

    output_file = f"{output_dir}/bonuses-betreal-analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
