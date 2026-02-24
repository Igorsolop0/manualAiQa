#!/usr/bin/env python3
import requests
import json
import base64

# TestRail API configuration
TESTRAIL_URL = "https://nexttcode.testrail.io"
EMAIL = "ihor.so@nextcode.tech"
API_KEY = "WI8RMbuUOuOgsqFwVx2C-7y4HBmZrSolpj1SK9TbT"

# Auth header
auth_string = f"{EMAIL}:{API_KEY}"
auth_bytes = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {auth_bytes}",
    "Content-Type": "application/json"
}

def get_sections(project_id, suite_id):
    """Get all sections in a suite"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_cases(project_id, suite_id, section_id=None):
    """Get all test cases in a section"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}"
    if section_id:
        url += f"&section_id={section_id}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_case(case_id):
    """Get a specific test case"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_case/{case_id}"
    response = requests.get(url, headers=headers)
    return response.json()

# Project ID from URL: suites/view/631 → project_id is typically 1 or different
# Let's try to get sections from suite 631
print("Getting sections from TestRail...")

# First, let's find the project
# Usually project_id is in the URL or we can get all projects
url = f"{TESTRAIL_URL}/index.php?/api/v2/get_projects"
response = requests.get(url, headers=headers)
projects = response.json()

print("\n=== Projects ===")
for project in projects:
    print(f"ID: {project['id']}, Name: {project['name']}")
    
    # Get suites for this project
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_suites/{project['id']}"
    suites_response = requests.get(url, headers=headers)
    suites = suites_response.json()
    
    print(f"\n  Suites for {project['name']}:")
    for suite in suites:
        print(f"    Suite ID: {suite['id']}, Name: {suite['name']}")
        
        # Check if this is suite 631
        if suite['id'] == 631:
            print(f"\n  === FOUND SUITE 631 ===")
            print(f"  Project ID: {project['id']}")
            
            # Get sections for this suite
            sections = get_sections(project['id'], suite['id'])
            print(f"\n  Sections in Suite 631:")
            for section in sections:
                print(f"    Section ID: {section['id']}, Name: {section['name']}, Parent: {section.get('parent_id', 'None')}")
                
                # If this is "Footer" or "Regular Bonuses Section", get cases
                if 'Footer' in section['name'] or 'Regular Bonuses' in section['name']:
                    print(f"\n    Getting cases for section: {section['name']}")
                    cases = get_cases(project['id'], suite['id'], section['id'])
                    
                    if isinstance(cases, list):
                        for case in cases:
                            print(f"      Case ID: {case['id']}, Title: {case['title']}")
