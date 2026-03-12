#!/usr/bin/env python3
"""
Get bonuses with trigger: promocode from PROD environment.
"""

import requests
import json
import sys
from pathlib import Path

# Load env file
env_file = Path("/Users/ihorsolopii/Documents/minebit-e2e-playwright/.env.prod")
if not env_file.exists():
    print("❌ .env.prod not found")
    sys.exit(1)

# Parse env file
env_vars = {}
with open(env_file) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip()

# API configuration
API_BASE = env_vars.get("BACKOFFICE_API_URL", "https://adminwebapi.prod.sofon.one/api")
# BackOffice API uses UserId header for auth (no login needed)
USER_ID = 560  # PROD user ID

print(f"🌐 API Base: {API_BASE}")
print(f"👤 User ID: {USER_ID}")

# Setup session with UserId header
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Accept": "application/json",
    "UserId": str(USER_ID)
})

print(f"✅ Auth configured (UserId header)")

# Step 2: Get bonus campaigns
print(f"\n🎁 Fetching bonus campaigns...")

# Try different possible endpoints
endpoints = [
    "/Bonus/GetBonuses",  # Found in Swagger
    "/Content/GetPromotions",  # Promotions endpoint
    "/Bonus/GetBonusesForManualClaim",
]

campaigns = None
working_endpoint = None

for endpoint in endpoints:
    url = f"{API_BASE}{endpoint}"
    print(f"   Trying: {endpoint}")
    try:
        # Most BackOffice endpoints use POST with empty body
        response = session.post(url, json={})
        if response.status_code == 200:
            campaigns = response.json()
            working_endpoint = endpoint
            print(f"   ✅ Success!")
            break
        elif response.status_code == 404:
            continue
        else:
            print(f"   ⚠️ Status: {response.status_code}")
            # Try GET as fallback
            response = session.get(url)
            if response.status_code == 200:
                campaigns = response.json()
                working_endpoint = endpoint
                print(f"   ✅ Success (GET)!")
                break
    except Exception as e:
        print(f"   ❌ Error: {e}")

if not campaigns:
    print("\n❌ Could not find bonus campaigns endpoint")
    print("   Trying GraphQL...")

    # Try GraphQL
    graphql_url = "https://minebit-casino.prod.sofon.one/graphql"
    query = """
    query GetBonusCampaigns {
      bonusCampaigns {
        id
        name
        triggerType
        status
      }
    }
    """

    try:
        response = session.post(graphql_url, json={"query": query})
        if response.status_code == 200:
            result = response.json()
            if "data" in result and "bonusCampaigns" in result["data"]:
                campaigns = result["data"]["bonusCampaigns"]
                print(f"   ✅ Got {len(campaigns)} campaigns via GraphQL")
    except Exception as e:
        print(f"   ❌ GraphQL error: {e}")

if not campaigns:
    print("\n❌ No campaigns found")
    sys.exit(1)

# Debug: print structure
print(f"\n📊 Response type: {type(campaigns)}")
if isinstance(campaigns, dict):
    print(f"   Keys: {list(campaigns.keys())[:10]}")
    # Check for nested data
    for key in ['ResponseObject', 'bonuses', 'Bonuses', 'items', 'Items', 'data', 'Data']:
        if key in campaigns:
            campaigns = campaigns[key]
            print(f"   Found nested key: {key}")
            print(f"   Nested type: {type(campaigns)}")
            if isinstance(campaigns, dict):
                print(f"   Nested keys: {list(campaigns.keys())[:10]}")
                # Check for Entities (pagination structure)
                if 'Entities' in campaigns:
                    total_count = campaigns.get('Count', 'unknown')
                    campaigns = campaigns['Entities']
                    print(f"   ✅ Extracted {len(campaigns)} entities (Total count: {total_count})")
            elif isinstance(campaigns, list):
                print(f"   List length: {len(campaigns)}")
            break

print(f"\n📊 Total campaigns: {len(campaigns) if isinstance(campaigns, list) else 'still dict'}")

# Show first campaign structure
if isinstance(campaigns, list) and len(campaigns) > 0:
    print(f"\n📋 First campaign structure:")
    first = campaigns[0]
    print(json.dumps(first, indent=2)[:500])

# Step 3: Filter by trigger = promocode
print(f"\n🔍 Filtering by trigger: promocode...")

if isinstance(campaigns, list):
    promocode_bonuses = []
    for campaign in campaigns:
        # Check different possible field names
        trigger = campaign.get("triggerType") or campaign.get("TriggerType") or campaign.get("trigger_type") or campaign.get("Trigger")
        promo_code = campaign.get("PromoCode") or campaign.get("promoCode") or campaign.get("promo_code")
        
        # Filter: has promocode OR trigger contains 'promo'
        if (trigger and "promo" in str(trigger).lower()) or (promo_code and promo_code.strip()):
            campaign['_hasPromoCode'] = bool(promo_code)
            campaign['_triggerType'] = trigger if trigger else 'promocode'
            promocode_bonuses.append(campaign)
elif isinstance(campaigns, dict):
    # Might be nested
    if "campaigns" in campaigns:
        campaigns = campaigns["campaigns"]
    elif "Campaigns" in campaigns:
        campaigns = campaigns["Campaigns"]
    elif "items" in campaigns:
        campaigns = campaigns["items"]

    promocode_bonuses = []
    for campaign in campaigns if isinstance(campaigns, list) else []:
        trigger = campaign.get("triggerType") or campaign.get("TriggerType") or campaign.get("trigger_type") or campaign.get("Trigger")
        if trigger and "promo" in str(trigger).lower():
            promocode_bonuses.append(campaign)

print(f"✅ Found {len(promocode_bonuses)} bonuses with trigger: promocode")

# Step 4: Save results
output_file = Path("/Users/ihorsolopii/.openclaw/workspace/shared/test-results/CT-603/bonuses-promocode.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w") as f:
    json.dump({
        "total_campaigns": len(campaigns) if isinstance(campaigns, list) else "unknown",
        "promocode_bonuses_count": len(promocode_bonuses),
        "promocode_bonuses": promocode_bonuses
    }, f, indent=2)

print(f"\n💾 Results saved to: {output_file}")

# Print summary
if promocode_bonuses:
    print(f"\n📋 Promocode Bonuses Summary:")
    for i, bonus in enumerate(promocode_bonuses[:10], 1):  # Show first 10
        print(f"\n   {i}. {bonus.get('name') or bonus.get('Name') or bonus.get('campaignName', 'Unknown')}")
        print(f"      ID: {bonus.get('id') or bonus.get('Id') or bonus.get('campaignId', 'N/A')}")
        print(f"      Trigger: {bonus.get('triggerType') or bonus.get('TriggerType', 'N/A')}")
        print(f"      Status: {bonus.get('status') or bonus.get('Status') or bonus.get('isActive', 'N/A')}")

    if len(promocode_bonuses) > 10:
        print(f"\n   ... and {len(promocode_bonuses) - 10} more")
else:
    print("\n⚠️ No bonuses with trigger: promocode found")
    print("\n📋 All campaigns (first 5):")
    for i, campaign in enumerate(campaigns[:5] if isinstance(campaigns, list) else [], 1):
        print(f"\n   {i}. {campaign.get('name') or campaign.get('Name', 'Unknown')}")
        print(f"      Trigger: {campaign.get('triggerType') or campaign.get('TriggerType', 'N/A')}")
