#!/usr/bin/env python3
"""
Check if a daily tracker entry exists for today.
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

# Load Notion API key
api_key_path = Path.home() / '.config' / 'notion' / 'api_key'
if not api_key_path.exists():
    print(f"❌ Notion API key not found at {api_key_path}")
    exit(1)

with open(api_key_path, 'r') as f:
    NOTION_KEY = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

def load_tracker_info():
    """Load database ID and data source ID from info file."""
    info_file = Path(__file__).parent / 'daily_tracker_info.json'
    if not info_file.exists():
        print(f"❌ Daily tracker info not found: {info_file}")
        exit(1)
    
    with open(info_file, 'r') as f:
        data = json.load(f)
        return data.get('database_id'), data.get('data_source_id')

def query_today_entries(data_source_id):
    """Query database for entries with today's date."""
    today = datetime.now(timezone.utc).date().isoformat()
    
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    
    filter_data = {
        "filter": {
            "property": "Date",
            "date": {
                "equals": today
            }
        },
        "sorts": [{"property": "Date", "direction": "descending"}]
    }
    
    response = requests.post(url, headers=HEADERS, json=filter_data)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return results
    else:
        print(f"❌ Query failed: {response.status_code}")
        print(response.text)
        return []

def main():
    print("📅 Checking daily tracker entries for today...")
    
    # Load IDs
    database_id, data_source_id = load_tracker_info()
    if not database_id or not data_source_id:
        print("❌ Missing database_id or data_source_id")
        exit(1)
    
    print(f"📊 Database ID: {database_id}")
    print(f"🔍 Data source ID: {data_source_id}")
    
    # Query for today's entries
    entries = query_today_entries(data_source_id)
    
    if entries:
        print(f"✅ Found {len(entries)} entry/entries for today")
        for entry in entries:
            props = entry.get('properties', {})
            date = props.get('Date', {}).get('date', {}).get('start', 'No date')
            sleep = props.get('Sleep Hours', {}).get('number', 'No sleep')
            print(f"   • Date: {date}, Sleep: {sleep}")
        return True
    else:
        print("📝 No entry found for today")
        return False

if __name__ == "__main__":
    exists = main()
    # Exit with code 0 if entry exists, 1 if not
    exit(0 if exists else 1)