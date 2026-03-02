#!/usr/bin/env python3
"""
Analyze TestRail test cases for Minebit and identify gaps in test coverage.
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path

# Load config
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
    print("❌ Missing TestRail configuration")
    sys.exit(1)

# Auth header
auth_string = f"{TESTRAIL_EMAIL}:{TESTRAIL_API_KEY}"
auth_bytes = base64.b64encode(auth_string.encode()).decode()
headers = {
    "Authorization": f"Basic {auth_bytes}",
    "Content-Type": "application/json"
}

def get_sections(project_id=1, suite_id=631):
    """Get all sections in Minebit suite."""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"❌ Failed to get sections: {response.status_code}")
        return []
    
    data = response.json()
    return data.get('sections', [])

def get_cases_for_section(project_id, suite_id, section_id):
    """Get test cases for a specific section."""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"❌ Failed to get cases for section {section_id}: {response.status_code}")
        return []
    
    data = response.json()
    return data.get('cases', [])

def analyze_section_coverage(sections):
    """Analyze test case coverage for each section."""
    print("🔍 Analyzing TestRail coverage for Minebit...")
    
    all_cases = []
    section_stats = {}
    
    for section in sections:
        section_id = section['id']
        section_name = section['name']
        parent_id = section.get('parent_id')
        depth = section['depth']
        
        # Get cases for this section
        cases = get_cases_for_section(1, 631, section_id)
        
        section_stats[section_id] = {
            'name': section_name,
            'depth': depth,
            'parent_id': parent_id,
            'case_count': len(cases),
            'cases': cases[:10]  # First 10 cases only
        }
        
        all_cases.extend(cases)
        
        # Print section summary
        indent = "  " * depth
        print(f"{indent}📂 {section_name} (ID: {section_id}): {len(cases)} cases")
    
    return section_stats, all_cases

def identify_gaps(section_stats, all_cases):
    """Identify gaps in test coverage based on Minebit functionality."""
    print("\n🔎 Identifying gaps in test coverage...")
    
    gaps = []
    
    # Check coverage by functional area
    functional_areas = {
        'authentication': ['login', 'registration', 'logout', 'password_reset', '2fa'],
        'bonuses': ['regular', 'special', 'welcome', 'promo_code', 'campaign'],
        'payments': ['deposit', 'withdrawal', 'crypto', 'balance', 'transactions'],
        'games': ['game_launch', 'demo_mode', 'providers', 'favorites', 'search'],
        'profile': ['personal_info', 'kyc', 'verification', 'account_settings'],
        'ui_components': ['sidebar', 'footer', 'header', 'wallet_modal', 'mobile']
    }
    
    # Analyze what we have
    existing_coverage = {}
    for section_id, stats in section_stats.items():
        section_name = stats['name'].lower()
        case_count = stats['case_count']
        
        # Map to functional areas
        for area, keywords in functional_areas.items():
            for keyword in keywords:
                if keyword in section_name:
                    existing_coverage[area] = existing_coverage.get(area, 0) + case_count
    
    # Identify missing areas
    print("\n📊 Existing Coverage by Area:")
    for area in functional_areas.keys():
        coverage = existing_coverage.get(area, 0)
        print(f"  {area.capitalize()}: {coverage} test cases")
        
        if coverage < 5:  # Arbitrary threshold
            gaps.append({
                'area': area,
                'reason': f'Low test coverage ({coverage} cases) for {area}',
                'recommendations': [
                    f'Add more test cases for {area} functionality',
                    f'Consider adding automated tests for critical {area} flows'
                ]
            })
    
    # Check for specific missing test types
    critical_test_types = [
        'API testing',
        'Performance testing',
        'Security testing',
        'Mobile-specific testing',
        'Cross-browser compatibility',
        'Error handling',
        'Edge cases',
        'Localization testing'
    ]
    
    # Check if we have any API-focused tests
    api_test_count = 0
    for case in all_cases:
        title = case.get('title', '').lower()
        if 'api' in title or 'endpoint' in title or 'request' in title:
            api_test_count += 1
    
    if api_test_count < 3:
        gaps.append({
            'area': 'api_testing',
            'reason': f'Only {api_test_count} API-focused test cases found',
            'recommendations': [
                'Add API test cases for critical endpoints (Website API, BackOffice API)',
                'Test authentication flows via API',
                'Test error responses and edge cases for APIs'
            ]
        })
    
    # Check for mobile testing
    mobile_test_count = 0
    for case in all_cases:
        title = case.get('title', '').lower()
        if 'mobile' in title or 'responsive' in title or 'tablet' in title:
            mobile_test_count += 1
    
    if mobile_test_count < 5:
        gaps.append({
            'area': 'mobile_testing',
            'reason': f'Only {mobile_test_count} mobile-specific test cases found',
            'recommendations': [
                'Add mobile-specific UI test cases',
                'Test touch interactions on mobile devices',
                'Test mobile-optimized flows (deposit, game launch)'
            ]
        })
    
    # Check for payment system testing
    payment_keywords = ['deposit', 'withdrawal', 'payment', 'transaction', 'balance', 'wallet']
    payment_test_count = 0
    for case in all_cases:
        title = case.get('title', '').lower()
        if any(keyword in title for keyword in payment_keywords):
            payment_test_count += 1
    
    if payment_test_count < 10:
        gaps.append({
            'area': 'payment_testing',
            'reason': f'Only {payment_test_count} payment-related test cases found (critical for casino)',
            'recommendations': [
                'Add more test cases for deposit flows (various payment methods)',
                'Test withdrawal scenarios (KYC requirements, limits)',
                'Test crypto payment flows',
                'Test balance calculations and transactions'
            ]
        })
    
    return gaps

def recommend_new_tests(gaps, section_stats):
    """Recommend specific new test cases to add."""
    print("\n💡 Recommended New Test Cases:")
    
    recommendations = []
    
    # Based on gaps, recommend specific tests
    for gap in gaps:
        area = gap['area']
        
        if area == 'api_testing':
            recommendations.extend([
                "API: Test Website API authentication flow",
                "API: Test BackOffice API bonus creation",
                "API: Test Wallet API balance operations",
                "API: Test GraphQL registration mutation",
                "API: Test error handling for invalid API requests"
            ])
        
        elif area == 'payment_testing':
            recommendations.extend([
                "Payment: Test deposit with credit card (success and failure)",
                "Payment: Test crypto deposit (BTC, ETH, USDT)",
                "Payment: Test withdrawal with KYC verification",
                "Payment: Test minimum/maximum deposit limits",
                "Payment: Test balance synchronization after transactions",
                "Payment: Test payment method selection UI"
            ])
        
        elif area == 'mobile_testing':
            recommendations.extend([
                "Mobile: Test responsive design on iPhone 13/14",
                "Mobile: Test touch gestures in game lobby",
                "Mobile: Test mobile-optimized payment flows",
                "Mobile: Test hamburger menu functionality",
                "Mobile: Test orientation changes (portrait/landscape)"
            ])
        
        elif area == 'bonuses':
            recommendations.extend([
                "Bonuses: Test bonus activation with insufficient wagering",
                "Bonuses: Test bonus expiration logic",
                "Bonuses: Test parallel bonus claims (CT-45 scenario)",
                "Bonuses: Test bonus cancellation/revocation",
                "Bonuses: Test bonus history and tracking"
            ])
    
    # Add critical missing tests based on casino domain
    critical_casino_tests = [
        "Game: Test game launch with different providers (Pragmatic, Evolution, etc.)",
        "Game: Test demo mode functionality",
        "Game: Test game search and filtering",
        "Security: Test session timeout and re-authentication",
        "Security: Test XSS and injection vulnerabilities on forms",
        "Performance: Test page load times for game lobby",
        "Localization: Test language switching functionality",
        "Compliance: Test responsible gambling features",
        "KYC: Test document upload and verification flow",
        "Notifications: Test in-game notifications and alerts"
    ]
    
    recommendations.extend(critical_casino_tests)
    
    # Print recommendations
    for i, rec in enumerate(recommendations[:20], 1):
        print(f"  {i}. {rec}")
    
    return recommendations

def generate_testrail_import_format(recommendations):
    """Generate TestRail import format for recommended tests."""
    print("\n📝 TestRail Import Format (sample):")
    print("=" * 80)
    
    template = """
Section: {section}
Title: {title}
Type: Functional
Priority: {priority}
Estimate: 15m
Preconditions:
- User is authenticated (unless specified otherwise)
- Test environment is set up (QA/Dev)
- Required test data is prepared

Steps:
1. Navigate to the relevant page/feature
2. Perform the action described in the title
3. Verify expected result

Expected Results:
- Feature behaves as per requirements
- No errors or unexpected behavior
- UI elements are correctly displayed
"""
    
    # Group by category
    categories = {}
    for rec in recommendations[:10]:
        # Extract category from first word
        if ": " in rec:
            category, title = rec.split(": ", 1)
        else:
            category = "General"
            title = rec
        
        if category not in categories:
            categories[category] = []
        categories[category].append(title)
    
    for category, titles in categories.items():
        print(f"\n📂 Section: {category}")
        for title in titles[:3]:
            priority = "High" if "Security" in title or "Payment" in title else "Medium"
            print(f"\n  Test Case: {title}")
            print(f"  Priority: {priority}")
            print(f"  Automation: Candidate for Playwright automation")
    
    return categories

def main():
    print("🎰 Minebit TestRail Coverage Analysis")
    print("=" * 60)
    
    # Get sections
    sections = get_sections()
    if not sections:
        print("❌ No sections found")
        sys.exit(1)
    
    print(f"✅ Found {len(sections)} sections in Minebit suite")
    
    # Analyze coverage
    section_stats, all_cases = analyze_section_coverage(sections)
    
    print(f"\n📊 Total test cases found: {len(all_cases)}")
    
    # Identify gaps
    gaps = identify_gaps(section_stats, all_cases)
    
    print(f"\n🔴 Found {len(gaps)} significant gaps in test coverage")
    
    # Recommend new tests
    recommendations = recommend_new_tests(gaps, section_stats)
    
    # Generate import format
    generate_testrail_import_format(recommendations)
    
    # Save analysis
    analysis = {
        'total_sections': len(sections),
        'total_cases': len(all_cases),
        'gaps': gaps,
        'recommendations': recommendations[:30],
        'section_summary': {k: {'name': v['name'], 'case_count': v['case_count']} 
                           for k, v in section_stats.items()}
    }
    
    output_file = Path(__file__).parent / 'testrail_gap_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n💾 Analysis saved to: {output_file}")
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()