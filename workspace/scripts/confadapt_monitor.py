#!/usr/bin/env python3
"""
ConfAdapt Technology Monitor
Weekly check for updates on multi-token prediction / ConfAdapt research.
Checks:
1. arXiv paper updates (version changes)
2. GitHub repository existence
3. New related papers
"""

import os
import json
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# Configuration
WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = WORKSPACE / "memory" / "confadapt_state.json"
LOG_FILE = WORKSPACE / "memory" / "confadapt_log.md"

# URLs to monitor
ARXIV_PAPER_ID = "2602.06019"
ARXIV_API_URL = f"http://export.arxiv.org/api/query?id_list={ARXIV_PAPER_ID}"
GITHUB_REPO_URL = "https://github.com/jwkirchenbauer/confadapt"
ARXIV_SEARCH_URL = "http://export.arxiv.org/api/query?search_query=all:confadapt+OR+all:%22multi-token+prediction%22&start=0&max_results=10"

def load_state():
    """Load previous monitoring state"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "last_check": None,
        "arxiv_version": None,
        "arxiv_versions": [],
        "github_exists": False,
        "new_papers": [],
        "last_notification": None
    }

def save_state(state):
    """Save monitoring state"""
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def fetch_arxiv():
    """Fetch arXiv paper info"""
    try:
        with urllib.request.urlopen(ARXIV_API_URL, timeout=10) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        print(f"Error fetching arXiv: {e}")
        return None

def parse_arxiv_version(xml_content):
    """Extract version and update date from arXiv XML"""
    if not xml_content:
        return None, None
    
    # Simple parsing - look for version
    import re
    # Find version in <arxiv:version> tag
    version_match = re.search(r'<arxiv:version>(\d+)</arxiv:version>', xml_content)
    version = version_match.group(1) if version_match else "1"
    
    # Find updated date
    updated_match = re.search(r'<updated>([^<]+)</updated>', xml_content)
    updated = updated_match.group(1) if updated_match else None
    
    # Find title
    title_match = re.search(r'<title>([^<]+)</title>', xml_content)
    title = title_match.group(1) if title_match else "Unknown"
    
    return {
        "version": version,
        "updated": updated,
        "title": title.strip()
    }

def check_github():
    """Check if GitHub repo exists"""
    try:
        req = urllib.request.Request(GITHUB_REPO_URL, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        else:
            print(f"GitHub check error: {e}")
            return False
    except Exception as e:
        print(f"GitHub check error: {e}")
        return False

def search_new_papers():
    """Search for new related papers on arXiv"""
    try:
        with urllib.request.urlopen(ARXIV_SEARCH_URL, timeout=10) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return None

def parse_new_papers(xml_content):
    """Extract new papers from search results"""
    if not xml_content:
        return []
    
    import re
    papers = []
    
    # Find all entry tags
    entries = re.findall(r'<entry>(.*?)</entry>', xml_content, re.DOTALL)
    
    for entry in entries:
        # Extract ID
        id_match = re.search(r'<id>([^<]+)</id>', entry)
        if not id_match:
            continue
        
        paper_id = id_match.group(1)
        # Extract arXiv ID from URL
        arxiv_id_match = re.search(r'arxiv\.org/abs/([\d\.v]+)', paper_id)
        if arxiv_id_match:
            arxiv_id = arxiv_id_match.group(1)
        else:
            continue
        
        # Skip the main paper we're monitoring
        if ARXIV_PAPER_ID in arxiv_id:
            continue
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', entry)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        # Extract published date
        published_match = re.search(r'<published>([^<]+)</published>', entry)
        published = published_match.group(1) if published_match else None
        
        # Extract summary
        summary_match = re.search(r'<summary>([^<]+)</summary>', entry)
        summary = summary_match.group(1).strip() if summary_match else ""
        
        papers.append({
            "id": arxiv_id,
            "title": title,
            "published": published,
            "summary": summary[:200] + "..." if len(summary) > 200 else summary
        })
    
    return papers

def log_message(message):
    """Log message to log file"""
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"## {timestamp}\n{message}\n\n"
    
    # Read existing log and prepend new entry
    existing = ""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            existing = f.read()
    
    with open(LOG_FILE, 'w') as f:
        f.write(log_entry + existing)
    
    print(message)

def generate_report(state, new_state, changes):
    """Generate a report for notification"""
    report_lines = []
    report_lines.append("🔬 **ConfAdapt Technology Monitor**")
    report_lines.append(f"*Weekly check: {datetime.now().strftime('%Y-%m-%d')}*")
    report_lines.append("")
    
    if changes:
        report_lines.append("📈 **CHANGES DETECTED:**")
        
        if changes.get("arxiv_version_updated"):
            old_ver = state.get("arxiv_version", {}).get("version", "unknown")
            new_ver = new_state["arxiv_version"]["version"]
            report_lines.append(f"  • arXiv paper updated: v{old_ver} → v{new_ver}")
            if new_state["arxiv_version"].get("updated"):
                report_lines.append(f"    Updated: {new_state['arxiv_version']['updated']}")
        
        if changes.get("github_now_exists"):
            report_lines.append(f"  • GitHub repository is now accessible!")
        
        if changes.get("new_related_papers"):
            count = len(changes["new_related_papers"])
            report_lines.append(f"  • {count} new related paper(s) found:")
            for paper in changes["new_related_papers"][:3]:  # Show first 3
                report_lines.append(f"    • [{paper['id']}] {paper['title']}")
            if count > 3:
                report_lines.append(f"    ... and {count-3} more")
    
    else:
        report_lines.append("✅ **No significant changes detected.**")
    
    # Current status
    report_lines.append("")
    report_lines.append("📊 **CURRENT STATUS:**")
    report_lines.append(f"  • arXiv paper: v{new_state['arxiv_version']['version'] if new_state['arxiv_version'] else 'unknown'}")
    report_lines.append(f"  • GitHub repo: {'✅ Accessible' if new_state['github_exists'] else '❌ Not found'}")
    report_lines.append(f"  • Related papers tracked: {len(new_state.get('new_papers', []))}")
    
    report_lines.append("")
    report_lines.append("🔗 **Links:**")
    report_lines.append(f"  • Paper: https://arxiv.org/abs/{ARXIV_PAPER_ID}")
    report_lines.append(f"  • GitHub: {GITHUB_REPO_URL}")
    
    return "\n".join(report_lines)

def main():
    """Main monitoring function"""
    print(f"ConfAdapt Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load previous state
    state = load_state()
    new_state = state.copy()
    changes = {}
    
    # Check arXiv paper
    print("Checking arXiv paper...")
    arxiv_xml = fetch_arxiv()
    arxiv_info = parse_arxiv_version(arxiv_xml) if arxiv_xml else None
    
    if arxiv_info:
        new_state["arxiv_version"] = arxiv_info
        
        # Check if version changed
        if state.get("arxiv_version") and state["arxiv_version"].get("version") != arxiv_info["version"]:
            changes["arxiv_version_updated"] = True
            print(f"  Version changed: {state['arxiv_version'].get('version')} -> {arxiv_info['version']}")
        
        # Track version history
        if arxiv_info not in new_state.get("arxiv_versions", []):
            new_state.setdefault("arxiv_versions", []).append(arxiv_info)
    
    # Check GitHub
    print("Checking GitHub repository...")
    github_exists = check_github()
    new_state["github_exists"] = github_exists
    
    if not state.get("github_exists") and github_exists:
        changes["github_now_exists"] = True
        print("  GitHub repo now accessible!")
    
    # Search for new related papers
    print("Searching for related papers...")
    search_xml = search_new_papers()
    new_papers = parse_new_papers(search_xml) if search_xml else []
    
    # Find papers that are new since last check
    existing_ids = [p["id"] for p in state.get("new_papers", [])]
    truly_new = [p for p in new_papers if p["id"] not in existing_ids]
    
    if truly_new:
        changes["new_related_papers"] = truly_new
        print(f"  Found {len(truly_new)} new related papers")
    
    new_state["new_papers"] = new_papers[:20]  # Keep only recent 20
    
    # Update timestamp
    new_state["last_check"] = datetime.now().isoformat()
    
    # Generate report
    report = generate_report(state, new_state, changes)
    
    # Log results
    log_message(report)
    
    # Save state
    save_state(new_state)
    
    # Print report for cron output
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    # Return report for notification
    return report, bool(changes)

if __name__ == "__main__":
    try:
        report, has_changes = main()
        
        # If running in OpenClaw cron, we can send notification
        # This part would be handled by the cron notification system
        sys.exit(0)
        
    except Exception as e:
        error_msg = f"❌ Monitor failed: {str(e)}"
        log_message(error_msg)
        print(error_msg)
        sys.exit(1)