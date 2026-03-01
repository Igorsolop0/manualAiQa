#!/usr/bin/env python3
"""
Script to list evidence artifacts for Jira ticket attachments.
This script only lists files - actual upload must be done manually in Jira UI.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

def list_artifacts(ticket_id: str, test_results_dir: str = "./test-results"):
    """List all evidence artifacts for a given ticket."""
    ticket_dir = Path(test_results_dir) / ticket_id
    
    if not ticket_dir.exists():
        print(f"❌ No test results found for ticket {ticket_id}")
        print(f"   Expected directory: {ticket_dir}")
        return None
    
    artifacts = {
        "screenshots": [],
        "videos": [],
        "traces": [],
        "reports": []
    }
    
    # Screenshots
    screenshots_dir = ticket_dir / "screenshots"
    if screenshots_dir.exists():
        artifacts["screenshots"] = sorted([str(f) for f in screenshots_dir.glob("*.png")])
    
    # Videos
    videos_dir = ticket_dir / "videos"
    if videos_dir.exists():
        artifacts["videos"] = sorted([str(f) for f in videos_dir.glob("*.webm")])
    
    # Traces
    traces_dir = ticket_dir / "traces"
    if traces_dir.exists():
        artifacts["traces"] = sorted([str(f) for f in traces_dir.glob("*.zip")])
    
    # HTML Reports
    report_dir = ticket_dir / "report"
    if report_dir.exists():
        html_reports = list(report_dir.glob("*.html"))
        if html_reports:
            artifacts["reports"] = [str(html_reports[0])]
    
    return artifacts

def generate_draft_comment(ticket_id: str, artifacts: dict) -> str:
    """Generate draft Jira comment with evidence listing."""
    passed_count = 0  # Would need to parse actual test results
    failed_count = 0
    skipped_count = 0
    
    # Count screenshots to estimate test counts
    passed_screenshots = [f for f in artifacts["screenshots"] if "PASSED" in f]
    failed_screenshots = [f for f in artifacts["screenshots"] if "FAILED" in f]
    
    passed_count = len(passed_screenshots)
    failed_count = len(failed_screenshots)
    total_count = passed_count + failed_count
    
    comment = f"""📋 DRAFT Jira Comment для {ticket_id}

🤖 QA Agent Report — {ticket_id}
✅ Passed: {passed_count} | ❌ Failed: {failed_count} | ⏭️ Skipped: {skipped_count}
⏱️ Duration: Xs

Evidence:
📸 Screenshots: {len(artifacts['screenshots'])} files
🎥 Video: {len(artifacts['videos'])} files
📊 Full HTML Report: ./test-results/{ticket_id}/report/index.html

Failed tests:"""
    
    # Add failed test details if available
    for screenshot in failed_screenshots:
        test_name = Path(screenshot).stem.replace(f"{ticket_id}-", "").replace("-FAILED", "")
        comment += f"\n- {test_name} → Причина: [error message] → Screenshot: {Path(screenshot).name}"
    
    if not failed_screenshots:
        comment += "\n- None"
    
    comment += "\n\nВисновок: Ready to merge / Needs fixes / Blocked"
    
    return comment

def main():
    parser = argparse.ArgumentParser(description="List evidence artifacts for Jira ticket")
    parser.add_argument("ticket_id", help="Jira ticket ID (e.g., CT-727)")
    parser.add_argument("--test-results-dir", default="./test-results", 
                       help="Path to test-results directory (default: ./test-results)")
    parser.add_argument("--generate-comment", action="store_true",
                       help="Generate draft Jira comment")
    
    args = parser.parse_args()
    
    print(f"🔍 Looking for evidence artifacts for ticket {args.ticket_id}")
    print(f"📁 Test results directory: {args.test_results_dir}")
    print("-" * 50)
    
    artifacts = list_artifacts(args.ticket_id, args.test_results_dir)
    
    if not artifacts:
        print("❌ No artifacts found. Make sure tests have been run.")
        sys.exit(1)
    
    # Print summary
    print("📊 Artifacts found:")
    print(f"  📸 Screenshots: {len(artifacts['screenshots'])}")
    if artifacts['screenshots']:
        print("     " + "\n     ".join(Path(f).name for f in artifacts['screenshots'][:3]))
        if len(artifacts['screenshots']) > 3:
            print(f"     ... and {len(artifacts['screenshots']) - 3} more")
    
    print(f"  🎥 Videos: {len(artifacts['videos'])}")
    if artifacts['videos']:
        print("     " + "\n     ".join(Path(f).name for f in artifacts['videos'][:3]))
    
    print(f"  📦 Traces: {len(artifacts['traces'])}")
    print(f"  📄 Reports: {len(artifacts['reports'])}")
    
    # Show full paths if needed
    if args.generate_comment:
        print("\n" + "=" * 50)
        print("📋 DRAFT JIRA COMMENT (copy and paste to Jira):")
        print("=" * 50)
        comment = generate_draft_comment(args.ticket_id, artifacts)
        print(comment)
        print("=" * 50)
        
        print("\n📎 Manual upload instructions:")
        print("1. Go to Jira ticket: https://next-t-code.atlassian.net/browse/" + args.ticket_id)
        print("2. Click 'Add attachment'")
        print("3. Upload all files from:")
        print(f"   {Path(args.test_results_dir) / args.ticket_id}")
        print("4. Paste the comment above")
        print("5. Add any additional context if needed")
    
    # Save artifacts list to JSON for reference
    output_file = Path(args.test_results_dir) / args.ticket_id / "artifacts.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump({
            "ticket_id": args.ticket_id,
            "timestamp": datetime.now().isoformat(),
            "artifacts": artifacts
        }, f, indent=2)
    
    print(f"\n✅ Artifacts list saved to: {output_file}")

if __name__ == "__main__":
    main()