#!/usr/bin/env python3
"""
Austria Telegram Channels Summary
Collects and summarizes posts from Austrian Ukrainian channels
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Channels to monitor
CHANNELS = [
    {
        "name": "Авточат Українці в Австрії",
        "username": "@cKdatJS0rFU1OWQy",
        "topics": ["проживання", "квартира", "іпотека", "страховка", "авто", "послуги", "RWR", "закони"]
    },
    {
        "name": "Австрія IT 🇦🇹 🇺🇦", 
        "username": "@austria_it_tg",
        "topics": ["IT", "робота", "QA", "вакансії", "податки", "RWR", "страховка", "перекази"]
    }
]

# Priority topics for filtering
PRIORITY_TOPICS = [
    # IT/Work
    "QA", "тестувальник", "тестув", "automation", "playwright", "selenium", "developer", "розробник",
    "вакансі", "робота", "job", "зарплата", "salary", "IT", "айтішник",
    # RWR
    "RWR", "rot-weiß-rot", "карта", "дозвіл", "перебування", "німецька", "німецьку",
    # Living
    "квартир", "оренд", "іпотек", "kaution", "kaucija", "wohnung", "проживан",
    # Insurance
    "страхов", "versicherung", "SVS", "соціальн", "пенсі",
    # Events/News
    "подія", "захід", "event", "зустріч", "громад", "українц",
    # Life hacks
    "лайфхак", "порад", "корисн", "підказ", "як отримат", "як зробит"
]

# State file
STATE_FILE = Path("/Users/ihorsolopii/.openclaw/workspace/.austria_summary_state.json")

def load_state():
    """Load last summary state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_summary": None, "last_messages": []}

def save_state(state):
    """Save summary state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_topic_summary():
    """
    Returns a summary request for the agent.
    The agent will use browser automation to fetch actual messages.
    """
    state = load_state()
    now = datetime.now()
    
    summary_request = {
        "channels": CHANNELS,
        "priority_topics": PRIORITY_TOPICS,
        "time": now.isoformat(),
        "last_summary": state.get("last_summary"),
        "instructions": """
Створи summary по цих каналах за останню добу.

ФОРМАТ SUMMARY:

🇦🇹 **AUSTRIA DAILY SUMMARY** (дата)

## 💼 IT/Робота (QA)
- [важливі вакансії, питання по роботі, податки]

## 🏠 Проживання
- [квартири, оренда, іпотека, кауціон]

## 📋 RWR/Документи
- [RWR карти, дозволи, страховки]

## 🎉 Події
- [заходи, зустрічі, новини громади]

## 💡 Лайфхаки
- [корисні поради, підказки]

## 📞 Контакти/Послуги
- [важливі контакти, послуги]

---
*Зібрано з: Авточат Українці в Австрії, Австрія IT*
"""
    }
    
    return summary_request

def main():
    """Main function - outputs JSON for the agent to process"""
    summary_request = get_topic_summary()
    print(json.dumps(summary_request, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
