#!/usr/bin/env python3
"""
Generate valid Telegram WebApp initData hash for testing.
Based on: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
"""

import hmac
import hashlib
import urllib.parse
import json
import argparse
from datetime import datetime


def generate_telegram_init_data(bot_token: str, user_id: int, username: str = "test_user", first_name: str = "Test"):
    """
    Generate valid Telegram WebApp initData for testing.
    
    Args:
        bot_token: Telegram bot token (from @BotFather)
        user_id: Telegram user ID (numeric)
        username: Telegram username (without @)
        first_name: User's first name
    
    Returns:
        URL-encoded query string with valid hash
    """
    
    # Create user object
    user_data = {
        "id": user_id,
        "first_name": first_name,
        "last_name": "User",
        "username": username,
        "language_code": "en"
    }
    
    # Create initData query string
    timestamp = int(datetime.now().timestamp())
    init_data = {
        "query_id": f"AAH{user_id}MQ{timestamp}",
        "user": json.dumps(user_data, separators=(',', ':')),  # Compact JSON
        "auth_date": str(timestamp),
    }
    
    # Sort and create data-check-string
    sorted_items = sorted(init_data.items())
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_items])
    
    # Generate hash
    # Step 1: Create secret key from bot token
    secret_key = hmac.new(
        b"WebAppData", 
        bot_token.encode(), 
        hashlib.sha256
    ).digest()
    
    # Step 2: Generate hash from data-check-string
    hash_value = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Add hash to init_data
    init_data["hash"] = hash_value
    
    # Return as URL-encoded query string
    return urllib.parse.urlencode(init_data)


def main():
    parser = argparse.ArgumentParser(description='Generate Telegram WebApp initData hash for testing')
    parser.add_argument('--bot-token', required=True, help='Telegram bot token')
    parser.add_argument('--user-id', type=int, required=True, help='Telegram user ID')
    parser.add_argument('--username', default='test_user', help='Telegram username')
    parser.add_argument('--first-name', default='Test', help='User first name')
    
    args = parser.parse_args()
    
    init_data = generate_telegram_init_data(
        bot_token=args.bot_token,
        user_id=args.user_id,
        username=args.username,
        first_name=args.first_name
    )
    
    print(init_data)


if __name__ == "__main__":
    main()
