import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime
import re

DEFAULT_JIRA_DOMAIN = "https://next-t-code.atlassian.net"
DEFAULT_JIRA_USER = "ihor.so@nextcode.tech"
DEFAULT_JIRA_TOKEN_PATH = "/Users/ihorsolopii/.openclaw/workspace/projects/nextcode/.jira_token"
DEFAULT_STATE_FILE = "/Users/ihorsolopii/.openclaw/workspace-jira-watcher/.jira_state.json"
DEFAULT_SHARED_CONTEXT_DIR = "/Users/ihorsolopii/.openclaw/workspace/shared/json-sources/jira"
DEFAULT_SLACK_CHANNEL = "C0AH10XDKM2"
DEFAULT_NEXUS_BOT_USER_ID = "U0AGXTVUU11"

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN", DEFAULT_JIRA_DOMAIN)
JIRA_USER = os.getenv("JIRA_USER", DEFAULT_JIRA_USER)
JIRA_TOKEN_PATH = os.getenv("JIRA_TOKEN_PATH", DEFAULT_JIRA_TOKEN_PATH)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "").strip()
SLACK_CHANNEL = os.getenv("JIRA_WATCHER_SLACK_CHANNEL", DEFAULT_SLACK_CHANNEL)
NEXUS_BOT_USER_ID = os.getenv("NEXUS_BOT_USER_ID", DEFAULT_NEXUS_BOT_USER_ID)
STATE_FILE = os.getenv("JIRA_WATCHER_STATE_FILE", DEFAULT_STATE_FILE)
SHARED_CONTEXT_DIR = os.getenv("JIRA_WATCHER_CONTEXT_DIR", DEFAULT_SHARED_CONTEXT_DIR)

JQL = 'project = "PandaSen" AND status IN ("Ready for testing", "On production") AND assignee = currentUser()'

def read_token():
    token = os.getenv("JIRA_API_TOKEN", "").strip()
    if token:
        return token
    if not os.path.exists(JIRA_TOKEN_PATH):
        raise Exception(f"Jira token not found at {JIRA_TOKEN_PATH}")
    with open(JIRA_TOKEN_PATH, "r") as f:
        return f.read().strip()

def jira_api_call(url, payload=None):
    token = read_token()
    auth_str = f"{JIRA_USER}:{token}"
    auth_header = "Basic " + base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8") if payload else None)
    req.add_header("Authorization", auth_header)
    req.add_header("Accept", "application/json")
    if payload:
        req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Jira API Error: {e.code} - {e.read().decode('utf-8')}")
        raise

def slack_post_message(blocks, text_fallback):
    if not SLACK_BOT_TOKEN:
        print("SLACK_BOT_TOKEN is missing; skipping Slack notification.")
        return

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": SLACK_CHANNEL,
        "text": text_fallback,
        "blocks": blocks
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if not res.get("ok"):
                print("Slack API Error:", res)
    except urllib.error.HTTPError as e:
        print(f"Slack HTTP Error: {e.code} - {e.read().decode('utf-8')}")

def extract_acceptance_criteria(description):
    if not description:
        return ""
    desc_str = json.dumps(description)
    # Simple extraction heuristic for ADF json
    match = re.search(r'(?i)(acceptance criteria|ac)[\s\S]*?(?=\n\n#|\n\n\*|\n\n$|$)', desc_str)
    if match:
        return "Found in description (ADF)"
    return "Not explicitly formatted, check full description."

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def main():
    print(f"[{datetime.now().isoformat()}] Starting Jira Watcher API poll...")
    
    state: dict = load_state()
    search_url = f"{JIRA_DOMAIN}/rest/api/3/search/jql"
    payload = {
        "jql": JQL,
        "fields": ["summary", "description", "comment", "issuelinks", "priority", "status", "updated"],
        "maxResults": 20
    }
    
    try:
        data = jira_api_call(search_url, payload)
    except Exception as e:
        print(f"Failed to query Jira: {e}")
        sys.exit(1)
    
    issues = data.get("issues", [])
    if not issues:
        print("No issues found matching JQL.")
        sys.exit(0)
    
    new_state = dict(state)
    updates = 0
    
    for issue in issues:
        key = issue["key"]
        fields = issue["fields"]
        updated = fields["updated"]
        status_name = fields["status"]["name"]
        
        # Check if we already processed this exact update
        last_updated = state.get(key)
        if last_updated == updated:
            continue
        
        # Extract fields securely
        summary = fields.get("summary", "No Summary")
        description = fields.get("description", {})
        priority = fields.get("priority", {}).get("name", "Unknown")
        
        print(f"New Update for {key}: {summary} (Status: {status_name})")
        updates += 1
        
        # Parse comments
        comments_data = fields.get("comment", {}).get("comments", [])
        last_comments = [c.get("body", {}) for c in comments_data[-5:]]
        
        # Parse links
        links = []
        for link in fields.get("issuelinks", []):
            if "outwardIssue" in link:
                direction = link["type"].get("outward", "relates to")
                links.append(f"{direction} {link['outwardIssue']['key']}")
            elif "inwardIssue" in link:
                direction = link["type"].get("inward", "is related to")
                links.append(f"{direction} {link['inwardIssue']['key']}")
        
        # Build advanced context JSON
        context = {
            "key": key,
            "url": f"{JIRA_DOMAIN}/browse/{key}",
            "summary": summary,
            "status": status_name,
            "priority": priority,
            "description": description,
            "acceptance_criteria": extract_acceptance_criteria(description),
            "recent_comments": last_comments,
            "linked_issues": links,
            "last_updated": updated
        }
        
        # Save Context File
        os.makedirs(SHARED_CONTEXT_DIR, exist_ok=True)
        context_file = os.path.join(SHARED_CONTEXT_DIR, f"{key}-context.json")
        with open(context_file, "w") as f:
            json.dump(context, f, indent=2)
            
        print(f"Saved context to {context_file}")
        
        # Prepare Slack Notification (Block Kit)
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 {key} is {status_name}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{JIRA_DOMAIN}/browse/{key}|{key}: {summary}>*\n"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Priority:*\n{priority}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Links:*\n{', '.join(links) if links else 'None'}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Context saved locally to: `{context_file}`\n\n<@{NEXUS_BOT_USER_ID}> Please analyze this ticket context using your Burger Methodology and provide a Test Plan for Ihor."
                }
            }
        ]
        
        fallback = f"{key} is {status_name}. Please analyze."
        
        slack_post_message(blocks, fallback)
        print(f"Slack notification sent for {key}")
        
        new_state[key] = updated

    if updates > 0:
        save_state(new_state)
    else:
        print("No new updates to process.")

if __name__ == "__main__":
    main()
