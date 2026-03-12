#!/usr/bin/env python3
"""Slack Message Helper - Allows sending messages and threaded replies directly via Slack API."""

import json
import sys
import argparse
import os
import urllib.request
import urllib.parse
from pathlib import Path

def get_slack_token():
    token = os.getenv("SLACK_BOT_TOKEN", "").strip()
    if token:
        return token

    config_path = Path.home() / ".openclaw" / "openclaw.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("channels", {}).get("slack", {}).get("botToken")
    except FileNotFoundError:
        return None

def main():
    parser = argparse.ArgumentParser(description="Send Slack messages via API")
    parser.add_argument("--channel", required=True, help="Slack Channel ID")
    parser.add_argument("--text", help="Fallback text message")
    parser.add_argument("--blocks", help="JSON string of Block Kit blocks")
    parser.add_argument("--thread_ts", help="Timestamp of parent message to reply in thread")
    
    args = parser.parse_args()
    token = get_slack_token()
    
    if not token:
        print(json.dumps({"error": "Slack bot token not found (set SLACK_BOT_TOKEN or configure openclaw.json)"}))
        sys.exit(1)

    payload = {
        "channel": args.channel
    }
    
    if args.text:
        payload["text"] = args.text
    if args.blocks:
        payload["blocks"] = json.loads(args.blocks)
    if args.thread_ts:
        payload["thread_ts"] = args.thread_ts

    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            if result.get("ok"):
                print(json.dumps({"ok": True, "ts": result.get("ts")}))
                sys.exit(0)
            else:
                print(json.dumps({"error": result.get("error")}))
                sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
