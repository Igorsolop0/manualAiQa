#!/usr/bin/env python3
"""
Test data generator utilities for Minebit/NextCode.
Provides functions for generating test emails, passwords, transaction IDs, etc.
"""

import random
import string
import time
import json
import yaml
from datetime import datetime
from pathlib import Path


def generate_email(ticket_id: str = None, prefix: str = "demo") -> str:
    """
    Generate a test email address.
    
    Args:
        ticket_id: Optional Jira ticket ID (e.g., "CT-727")
        prefix: Email prefix (default: "demo")
        
    Returns:
        Email address like demo1741035000@nextcode.tech
    """
    timestamp = int(time.time() * 1000)
    
    if ticket_id:
        # Clean ticket ID (remove spaces, special chars)
        clean_ticket = ticket_id.replace("-", "").replace(" ", "").upper()
        email = f"{prefix}{clean_ticket}{timestamp}@nextcode.tech"
    else:
        email = f"{prefix}{timestamp}@nextcode.tech"
    
    return email.lower()


def generate_password(length: int = 12, include_special: bool = True) -> str:
    """
    Generate a random password.
    
    Args:
        length: Password length
        include_special: Include special characters
        
    Returns:
        Random password like "Qweasd123!"
    """
    if include_special:
        # Use the default test password pattern
        return "Qweasd123!"
    
    # Alternative: generate random password
    letters = string.ascii_letters
    digits = string.digits
    special = "!@#$%^&*" if include_special else ""
    
    all_chars = letters + digits + special
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(digits),
    ]
    
    if include_special:
        password.append(random.choice(special))
    
    # Fill remaining length
    for _ in range(length - len(password)):
        password.append(random.choice(all_chars))
    
    # Shuffle
    random.shuffle(password)
    
    return "".join(password)


def generate_external_transaction_id(length: int = 20) -> str:
    """
    Generate a random external transaction ID.
    
    Args:
        length: Length of transaction ID
        
    Returns:
        Random transaction ID like "test_abc123def456"
    """
    chars = string.ascii_lowercase + string.digits
    random_part = "".join(random.choices(chars, k=length-5))
    return f"test_{random_part}"


def generate_client_data(ticket_id: str = None) -> dict:
    """
    Generate random client data for registration.
    
    Args:
        ticket_id: Optional Jira ticket ID
        
    Returns:
        Dictionary with client data
    """
    timestamp = int(time.time())
    
    # First names pool
    first_names = ["Test", "John", "Jane", "Alex", "Maria", "David", "Sarah"]
    
    # Last names pool  
    last_names = ["User", "Smith", "Johnson", "Brown", "Davis", "Wilson", "Taylor"]
    
    # Country codes
    countries = [
        {"code": "US", "id": 1, "name": "United States"},
        {"code": "GB", "id": 2, "name": "United Kingdom"},
        {"code": "DE", "id": 3, "name": "Germany"},
        {"code": "UA", "id": 4, "name": "Ukraine"},
    ]
    
    country = random.choice(countries)
    
    # Generate phone (fake but valid format)
    phone = f"+1{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    
    # Birth date (18-65 years old)
    current_year = datetime.now().year
    birth_year = random.randint(current_year - 65, current_year - 18)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    
    data = {
        "firstName": random.choice(first_names),
        "lastName": random.choice(last_names),
        "email": generate_email(ticket_id),
        "userName": f"demo{timestamp}{random.randint(100, 999)}",
        "password": generate_password(),
        "currencyId": "USD",
        "countryCode": country["code"],
        "countryId": country["id"],
        "phone": phone,
        "birthDate": f"{birth_year}-{birth_month:02d}-{birth_day:02d}",
        "timeZone": random.choice([-5, 0, 1, 2, 3]),  # Common timezones
        "languageId": "en",
        "termsConditionsAccepted": True,
        "sendPromotions": False,
        "sendSms": False,
        "sendMail": False,
        "deviceType": 1,  # Desktop
    }
    
    return data


def generate_deposit_data(client_id: int, amount: float = 100.0, currency: str = "USD") -> dict:
    """
    Generate deposit data for BackOffice API.
    
    Args:
        client_id: Client ID
        amount: Deposit amount
        currency: Currency code
        
    Returns:
        Dictionary with deposit data
    """
    return {
        "amount": amount,
        "clientId": client_id,
        "currencyId": currency,
        "externalTransactionId": generate_external_transaction_id(),
        "partnerPaymentMethodId": 19,  # Test payment method
        "paymentRequestType": "Deposit"
    }


def generate_bonus_data(
    bonus_type: str = "welcome",
    trigger_type: str = "deposit",
    client_id: int = None
) -> dict:
    """
    Generate bonus data for BackOffice API.
    
    Args:
        bonus_type: welcome, deposit, cashback, freespins
        trigger_type: deposit, promocode, campaign
        client_id: Optional client ID for targeting
        
    Returns:
        Dictionary with bonus data structure
    """
    bonus_templates = {
        "welcome": {
            "name": "Welcome Bonus 100%",
            "bonusTypeId": 1,  # Match Bonus
            "turnoverCount": 30,
            "minAmount": 10,
            "maxAmount": 100,
            "maxCashoutMultiplier": 10,
        },
        "deposit": {
            "name": "Deposit Bonus 50%",
            "bonusTypeId": 1,  # Match Bonus
            "turnoverCount": 20,
            "minAmount": 20,
            "maxAmount": 200,
            "maxCashoutMultiplier": 5,
        },
        "cashback": {
            "name": "Weekly Cashback",
            "bonusTypeId": 11,  # CampaignCash
            "turnoverCount": None,  # No wagering for cashback
            "minAmount": 0.3,
            "maxAmount": 1000,
            "maxCashoutMultiplier": None,
            "isSmartico": True,
        },
        "freespins": {
            "name": "Free Spins Bonus",
            "bonusTypeId": 2,  # Free Spins
            "turnoverCount": 0,
            "minAmount": 0,
            "maxAmount": 0,
            "freeSpinsCount": 20,
            "freeSpinsGameId": "pragmatic:123",
        }
    }
    
    template = bonus_templates.get(bonus_type, bonus_templates["welcome"])
    
    data = {
        "name": template["name"],
        "bonusTypeId": template["bonusTypeId"],
        "isActive": True,
        "isTest": True,
        "turnoverCount": template.get("turnoverCount"),
        "minAmount": template.get("minAmount", 0),
        "maxAmount": template.get("maxAmount", 0),
        "maxCashoutMultiplier": template.get("maxCashoutMultiplier"),
        "isSmartico": template.get("isSmartico", False),
    }
    
    # Add trigger-specific data
    if trigger_type == "deposit":
        data["triggerType"] = "AnyDeposit"
        data["minDepositAmount"] = 20
    elif trigger_type == "promocode":
        data["triggerType"] = "PromoCode"
        data["promoCode"] = f"TEST{random.randint(100, 999)}"
    elif trigger_type == "campaign":
        data["triggerType"] = "CampaignLink"
        data["campaignLink"] = f"/promo/test-{random.randint(1000, 9999)}"
    
    # Add client targeting if specified
    if client_id:
        data["clientIds"] = [client_id]
        data["segmentType"] = "SpecificClients"
    else:
        data["segmentType"] = "AllClients"
    
    return data


def load_config(env: str = "qa") -> dict:
    """
    Load configuration for specified environment.
    
    Args:
        env: Environment (dev, qa, prod)
        
    Returns:
        Configuration dictionary
    """
    config_path = Path(__file__).parent.parent / "config" / "environments.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    if env not in config["environments"]:
        raise ValueError(f"Unknown environment: {env}. Available: {list(config['environments'].keys())}")
    
    env_config = config["environments"][env].copy()
    env_config["common"] = config.get("common", {})
    
    return env_config


def save_test_data_log(entry: dict, log_file: str = "test_data_log.json"):
    """
    Save test data entry to log file for cleanup tracking.
    
    Args:
        entry: Test data entry (client, deposit, bonus, etc.)
        log_file: Log file name
    """
    log_path = Path(__file__).parent.parent / log_file
    
    entries = []
    if log_path.exists():
        try:
            with open(log_path) as f:
                entries = json.load(f)
        except json.JSONDecodeError:
            entries = []
    
    entry["created_at"] = datetime.now().isoformat()
    entries.append(entry)
    
    with open(log_path, "w") as f:
        json.dump(entries, f, indent=2)


def read_test_data_log(log_file: str = "test_data_log.json") -> list:
    """
    Read test data log.
    
    Args:
        log_file: Log file name
        
    Returns:
        List of test data entries
    """
    log_path = Path(__file__).parent.parent / log_file
    
    if not log_path.exists():
        return []
    
    with open(log_path) as f:
        return json.load(f)


if __name__ == "__main__":
    # Test the functions
    print("🧪 Test Data Generator - Sample Output")
    print("=" * 50)
    
    print(f"\n📧 Test email (no ticket): {generate_email()}")
    print(f"📧 Test email (with ticket): {generate_email('CT-727')}")
    
    print(f"\n🔐 Test password: {generate_password()}")
    
    print(f"\n💳 Transaction ID: {generate_external_transaction_id()}")
    
    print(f"\n👤 Client data sample:")
    client_data = generate_client_data()
    for key, value in list(client_data.items())[:5]:  # Show first 5 items
        print(f"  {key}: {value}")
    
    print(f"\n💰 Deposit data sample:")
    deposit_data = generate_deposit_data(123456)
    for key, value in deposit_data.items():
        print(f"  {key}: {value}")
    
    print(f"\n🎁 Bonus data sample (welcome):")
    bonus_data = generate_bonus_data("welcome", "deposit")
    for key, value in list(bonus_data.items())[:5]:
        print(f"  {key}: {value}")
    
    print(f"\n✅ Generator utilities ready!")