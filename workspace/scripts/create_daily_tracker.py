#!/usr/bin/env python3
"""
Create a Daily Tracker database in Notion for Ihor's habit tracking.
"""

import os
import json
import requests
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

def search_pages():
    """Search for pages to find Ihor's profile."""
    url = "https://api.notion.com/v1/search"
    data = {
        "filter": {"property": "object", "value": "page"},
        "page_size": 10
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code != 200:
        print(f"❌ Search failed: {response.status_code}")
        print(response.text)
        return None
    
    results = response.json().get('results', [])
    for page in results:
        title = page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'No title')
        if 'Ihor' in title or 'Profile' in title:
            return page['id']
    
    # If no Ihor profile found, return first page
    if results:
        return results[0]['id']
    
    return None

def create_daily_tracker(parent_page_id):
    """Create Daily Tracker database."""
    url = "https://api.notion.com/v1/databases"
    
    # Database properties
    properties = {
        "Date": {"date": {}},
        "Sleep Hours": {"number": {}},
        "Energy Givers": {"multi_select": {}},
        "Energy Takers": {"multi_select": {}},
        "Morning Activity": {"rich_text": {}},
        "Evening Routine": {"rich_text": {}},
        "Awareness": {"rich_text": {}},
        "Energy Level": {
            "select": {
                "options": [
                    {"name": "1 - Very Low", "color": "red"},
                    {"name": "2 - Low", "color": "orange"},
                    {"name": "3 - Medium", "color": "yellow"},
                    {"name": "4 - High", "color": "green"},
                    {"name": "5 - Very High", "color": "blue"}
                ]
            }
        },
        "Mood": {
            "select": {
                "options": [
                    {"name": "😊 Great", "color": "green"},
                    {"name": "🙂 Good", "color": "blue"},
                    {"name": "😐 Neutral", "color": "gray"},
                    {"name": "😔 Low", "color": "orange"},
                    {"name": "😞 Very Low", "color": "red"}
                ]
            }
        },
        "Notes": {"rich_text": {}}
    }
    
    data = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Daily Tracker - Habits & Energy"}}],
        "properties": properties,
        "is_inline": False
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Daily Tracker database created!")
        print(f"   Database ID: {result.get('id')}")
        print(f"   URL: https://notion.so/{result.get('id')}")
        return result
    else:
        print(f"❌ Failed to create database: {response.status_code}")
        print(response.text)
        return None

def main():
    print("🧠 Creating Daily Tracker database in Notion...")
    
    # Find parent page
    print("🔍 Searching for Ihor's profile page...")
    parent_page_id = search_pages()
    
    if not parent_page_id:
        print("❌ Could not find a suitable parent page")
        exit(1)
    
    print(f"📄 Found parent page ID: {parent_page_id}")
    
    # Create database
    db = create_daily_tracker(parent_page_id)
    
    if db:
        # Save database ID for future use
        db_id = db.get('id')
        
        tracker_info = {
            "database_id": db_id,
            "parent_page_id": parent_page_id,
            "properties": list(db.get('properties', {}).keys()),
            "created_at": db.get('created_time')
        }
        
        info_file = Path(__file__).parent / 'daily_tracker_info.json'
        with open(info_file, 'w') as f:
            json.dump(tracker_info, f, indent=2)
        
        print(f"💾 Database info saved to: {info_file}")
        print("\n📋 Properties created:")
        for prop in tracker_info['properties']:
            print(f"   • {prop}")
        
        print("\n🎯 Next steps:")
        print("   1. Share the database with your Notion integration if needed")
        print("   2. Daily conversations will start tomorrow at 22:00")
        print("   3. I'll ask questions and record your answers here")
        
        # Also save to workspace memory
        memory_file = Path(__file__).parent.parent / 'memory' / 'daily_tracker.md'
        memory_file.parent.mkdir(exist_ok=True)
        with open(memory_file, 'w') as f:
            f.write(f"""# Daily Tracker Database
Created: {tracker_info['created_at']}
Database ID: {db_id}
Parent Page ID: {parent_page_id}

## Purpose
Daily habit tracking for Ihor's 100-day journey reboot (2026-03-02 onward).

## Fields
- Date
- Sleep Hours
- Energy Givers (multi-select)
- Energy Takers (multi-select)
- Morning Activity
- Evening Routine
- Awareness
- Energy Level (1-5)
- Mood (😊/🙂/😐/😔/😞)
- Notes

## Conversation Time
22:00-22:20 daily
""")

if __name__ == "__main__":
    main()