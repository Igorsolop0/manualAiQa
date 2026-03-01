#!/usr/bin/env python3
"""Test TestRail API access and list available test cases for Minebit."""

import os
import sys
import base64
import requests
import json
from pathlib import Path

# Load config from .testrail_config
config_path = Path(__file__).parent.parent / '.testrail_config'
config = {}
with open(config_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

TESTRAIL_URL = config.get('TESTRAIL_URL')
TESTRAIL_EMAIL = config.get('TESTRAIL_EMAIL')
TESTRAIL_API_KEY = config.get('TESTRAIL_API_KEY')

if not all([TESTRAIL_URL, TESTRAIL_EMAIL, TESTRAIL_API_KEY]):
    print("❌ Missing TestRail configuration in .testrail_config")
    sys.exit(1)

# Auth header
auth_string = f"{TESTRAIL_EMAIL}:{TESTRAIL_API_KEY}"
auth_bytes = base64.b64encode(auth_string.encode()).decode()
headers = {
    "Authorization": f"Basic {auth_bytes}",
    "Content-Type": "application/json"
}

def test_api_access():
    """Test basic API access by fetching projects."""
    try:
        # First, try to get projects
        url = f"{TESTRAIL_URL}/index.php?/api/v2/get_projects"
        print(f"🔍 Testing TestRail API access to {TESTRAIL_URL}")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            projects = data.get('projects', [])
            print(f"✅ API access successful! Found {len(projects)} project(s)")
            return projects
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"   Raw response: {response.text[:200]}")
        return None

def list_projects(projects):
    """List all projects and their suites."""
    print("\n📁 TestRail Projects:")
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        print(f"  {project_id}. {project_name}")
        
        # Get suites for this project
        try:
            suites_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_suites/{project_id}"
            suites_response = requests.get(suites_url, headers=headers, timeout=30)
            
            if suites_response.status_code == 200:
                suites = suites_response.json()
                if suites:
                    print(f"     Suites:")
                    for suite in suites:
                        suite_id = suite['id']
                        suite_name = suite['name']
                        print(f"       - {suite_id}: {suite_name}")
                        
                        # Check if this is related to Minebit
                        if 'minebit' in suite_name.lower() or 'nextcode' in suite_name.lower():
                            print(f"         ⭐ Likely Minebit suite!")
                        
                        # Get sections for this suite
                        sections_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}"
                        sections_response = requests.get(sections_url, headers=headers, timeout=30)
                        if sections_response.status_code == 200:
                            sections = sections_response.json()
                            if sections:
                                print(f"         Sections: {len(sections)}")
                                # Show first 3 sections
                                for section in sections[:3]:
                                    print(f"           • {section['id']}: {section['name']}")
                                if len(sections) > 3:
                                    print(f"           ... and {len(sections) - 3} more")
            else:
                print(f"     Failed to get suites: {suites_response.status_code}")
                
        except Exception as e:
            print(f"     Error fetching suites: {e}")

def search_minebit_cases(projects):
    """Search for Minebit-related test cases."""
    print("\n🔍 Searching for Minebit test cases...")
    
    minebit_cases = []
    
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        
        # Check if project might be related to NextCode/Minebit
        if 'next' in project_name.lower() or 'code' in project_name.lower():
            print(f"\n  Looking in project: {project_name} (ID: {project_id})")
            
            # Get suites
            suites_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_suites/{project_id}"
            suites_response = requests.get(suites_url, headers=headers, timeout=30)
            
            if suites_response.status_code == 200:
                suites = suites_response.json()
                
                for suite in suites:
                    suite_id = suite['id']
                    suite_name = suite['name']
                    
                    # Look for sections
                    sections_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}"
                    sections_response = requests.get(sections_url, headers=headers, timeout=30)
                    
                    if sections_response.status_code == 200:
                        sections = sections_response.json()
                        
                        for section in sections:
                            section_id = section['id']
                            section_name = section['name']
                            
                            # Get cases in this section
                            cases_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}"
                            cases_response = requests.get(cases_url, headers=headers, timeout=30)
                            
                            if cases_response.status_code == 200:
                                cases = cases_response.json()
                                if cases and isinstance(cases, list) and len(cases) > 0:
                                    print(f"\n    📂 Section: {section_name} (ID: {section_id})")
                                    print(f"      Found {len(cases)} test case(s)")
                                    
                                    # Show first 5 cases
                                    for case in cases[:5]:
                                        print(f"      • TC-{case['id']}: {case['title']}")
                                    
                                    if len(cases) > 5:
                                        print(f"      ... and {len(cases) - 5} more")
                                    
                                    # Add to minebit cases
                                    for case in cases:
                                        minebit_cases.append({
                                            'project_id': project_id,
                                            'project_name': project_name,
                                            'suite_id': suite_id,
                                            'suite_name': suite_name,
                                            'section_id': section_id,
                                            'section_name': section_name,
                                            'case_id': case['id'],
                                            'case_title': case['title']
                                        })
    
    return minebit_cases

def main():
    print("🧪 TestRail API Access Check")
    print("=" * 50)
    
    # Test API access
    projects = test_api_access()
    if not projects:
        print("\n❌ Cannot access TestRail API. Check configuration and network.")
        sys.exit(1)
    
    # List all projects and suites
    list_projects(projects)
    
    # Search for Minebit cases
    minebit_cases = search_minebit_cases(projects)
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"✅ TestRail API: Accessible")
    print(f"📁 Total projects: {len(projects)}")
    print(f"🧪 Minebit-related test cases found: {len(minebit_cases)}")
    
    if minebit_cases:
        print("\n📍 Sample Minebit test cases:")
        for i, case in enumerate(minebit_cases[:10]):
            print(f"  {i+1}. TC-{case['case_id']}: {case['case_title']}")
            print(f"     Project: {case['project_name']}, Suite: {case['suite_name']}")
            print(f"     Section: {case['section_name']}")
    
    # Save summary for later use
    summary = {
        'testrail_url': TESTRAIL_URL,
        'email': TESTRAIL_EMAIL,
        'projects_count': len(projects),
        'minebit_cases_count': len(minebit_cases),
        'minebit_cases': minebit_cases[:20]  # First 20 only
    }
    
    output_file = Path(__file__).parent / 'testrail_summary.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Summary saved to: {output_file}")
    print("\n✅ TestRail check complete!")

if __name__ == "__main__":
    main()