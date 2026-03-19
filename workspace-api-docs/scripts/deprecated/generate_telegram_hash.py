#!/usr/bin/env python3
import hmac
import hashlib
import urllib.parse
import json
import argparse
from datetime import datetime

def generate_telegram_init_data(bot_token: str, user_id: int, username: str = "test_user"):
    """
    Generate valid Telegram WebApp initData for testing.
    Based on: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    
    # Create user object
    user_data = {
        "id": user_id,
        "first_name": f"Test{user_id}",
        "last_name": "User",
        "username": username,
        "language_code": "en"
    }
    
    # Create initData query string
    init_data = {
        "query_id": f"AAH{user_id}MQ{datetime.now().timestamp():.0f}",
        "user": json.dumps(user_data),
        "auth_date": str(int(datetime.now().timestamp())),
    }
    
    # Sort and create data-check-string
    sorted_items = sorted(init_data.items())
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_items])
    
    # Generate hash
    secret_key = hmac.new(
        b"WebAppData", 
        bot_token.encode(), 
        hashlib.sha256
    ).digest()
    
    hash_value = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Add hash to init_data
    init_data["hash"] = hash_value
    
    # Return as query string
    return urllib.parse.urlencode(init_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Telegram WebApp init data')
    parser.add_argument('--bot-token', required=True, help='Telegram bot token')
    parser.add_argument('--user-id', required=True, type=int, help='Telegram user ID')
    parser.add_argument('--username', default='testuser', help='Username (default: testuser)')
    
    args = parser.parse_args()
    
    init_data = generate_telegram_init_data(args.bot_token, args.user_id, args.username)
    print(init_data)
