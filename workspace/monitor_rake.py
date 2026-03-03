import requests
import json
import time

def monitor_bonuses():
    url = "https://websitewebapi.qa.sofon.one/5/api/v3/Bonus/GetBonuses"
    headers = {
        "Content-Type": "application/json",
        "website-locale": "en",
        "website-origin": "https://minebit-casino.qa.sofon.one",
        "x-time-zone-offset": "-60",
    }
    data = {
        "partnerId": 5,
        "languageId": "en",
        "timeZone": -60,
        "domain": "https://minebit-casino.qa.sofon.one",
        "token": "5c34ccdc70f94c10aa466fb27ec03d33"
    }
    
    print("🔍 Monitoring bonuses for player 3563249...")
    print("Press Ctrl+C to stop.\n")
    
    last_response = None
    while True:
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                bonuses = result.get("ResponseObject", [])
                if bonuses != last_response:
                    if bonuses:
                        print(f"[{time.strftime('%H:%M:%S')}] Found {len(bonuses)} bonus(es):")
                        for bonus in bonuses:
                            # Try to extract relevant fields
                            bonus_id = bonus.get('Id')
                            bonus_type = bonus.get('BonusType')
                            amount = bonus.get('Amount')
                            status = bonus.get('Status')
                            print(f"  - ID: {bonus_id}, Type: {bonus_type}, Amount: {amount}, Status: {status}")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] No bonuses yet")
                    last_response = bonuses
                else:
                    # No change, just show a dot
                    print(".", end="", flush=True)
            else:
                print(f"[{time.strftime('%H:%M:%S')}] HTTP error: {resp.status_code}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    monitor_bonuses()