#!/usr/bin/env python3
"""
Recipe: activate-bonus
Activate a bonus for a player via Smartico CRM Gateway.
Supports: promo code activation, manual bonus claim, and campaign assignment.
"""

import json
import sys

import requests

from env_config import (
    DEFAULT_BRAND,
    DEFAULT_ENV,
    crm_headers,
    get_brand,
    get_env,
)


def activate_promocode(
    client_id: int,
    promocode: str,
    env: str = DEFAULT_ENV,
) -> dict:
    """
    Activate a bonus via promo code through CRM Gateway (Smartico).

    Args:
        client_id: Player ID
        promocode: Bonus promo code (can be bonus ID string)
        env: Environment

    Returns:
        dict with keys: success, client_id, promocode, response
    """
    e = get_env(env)
    url = f"{e['crm_gateway']}/api/CRM/ActivatePromocode"

    data = {
        "ClientId": client_id,
        "Promocode": promocode,
    }

    resp = requests.post(url, headers=crm_headers(), json=data, timeout=30)

    result = {
        "success": resp.status_code == 200,
        "client_id": client_id,
        "promocode": promocode,
        "status_code": resp.status_code,
        "env": env,
    }

    try:
        body = resp.json()
        result["response"] = body
    except Exception:
        result["response_text"] = resp.text

    if resp.status_code != 200:
        print(f"[activate-bonus] FAILED: {resp.status_code} - {resp.text}")
    else:
        print(f"[activate-bonus] activated promocode={promocode} for client_id={client_id} env={env}")

    return result


def claim_campaign_bonus(
    client_id: int,
    bonus_id: int,
    env: str = DEFAULT_ENV,
) -> dict:
    """
    Claim a campaign bonus for a player via CRM Gateway (Smartico).

    Args:
        client_id: Player ID
        bonus_id: Bonus campaign ID
        env: Environment

    Returns:
        dict with keys: success, client_id, bonus_id, response
    """
    e = get_env(env)
    url = f"{e['crm_gateway']}/api/CRM/ClaimToCampaignBonus"

    data = {
        "ClientId": client_id,
        "BonusId": bonus_id,
    }

    resp = requests.post(url, headers=crm_headers(), json=data, timeout=30)

    result = {
        "success": resp.status_code == 200,
        "client_id": client_id,
        "bonus_id": bonus_id,
        "status_code": resp.status_code,
        "env": env,
    }

    try:
        body = resp.json()
        result["response"] = body
    except Exception:
        result["response_text"] = resp.text

    if resp.status_code != 200:
        print(f"[activate-bonus] FAILED: {resp.status_code} - {resp.text}")
    else:
        print(f"[activate-bonus] claimed bonus_id={bonus_id} for client_id={client_id} env={env}")

    return result


def get_bonus_campaigns(
    env: str = DEFAULT_ENV,
    bonus_ids: list = None,
) -> dict:
    """
    Get available bonus campaigns from CRM Gateway (Smartico).

    Args:
        env: Environment
        bonus_ids: Optional list of bonus IDs to filter

    Returns:
        dict with keys: success, campaigns
    """
    e = get_env(env)
    url = f"{e['crm_gateway']}/api/CRM/GetBonusCampaigns"

    data = {}
    if bonus_ids:
        data["FilterByBonusIds"] = bonus_ids

    resp = requests.post(url, headers=crm_headers(), json=data, timeout=30)

    result = {
        "success": resp.status_code == 200,
        "status_code": resp.status_code,
        "env": env,
    }

    try:
        body = resp.json()
        result["campaigns"] = body
    except Exception:
        result["response_text"] = resp.text

    if resp.status_code == 200:
        print(f"[activate-bonus] retrieved bonus campaigns env={env}")
    else:
        print(f"[activate-bonus] FAILED to get campaigns: {resp.status_code}")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Activate bonus via CRM Gateway")
    parser.add_argument("--client-id", type=int, help="Player ID")
    parser.add_argument("--promocode", help="Promo code to activate")
    parser.add_argument("--bonus-id", type=int, help="Bonus campaign ID to claim")
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--list-campaigns", action="store_true", help="List available bonus campaigns")
    args = parser.parse_args()

    if args.list_campaigns:
        result = get_bonus_campaigns(env=args.env)
    elif args.promocode and args.client_id:
        result = activate_promocode(args.client_id, args.promocode, env=args.env)
    elif args.bonus_id and args.client_id:
        result = claim_campaign_bonus(args.client_id, args.bonus_id, env=args.env)
    else:
        parser.error("Provide --client-id with --promocode or --bonus-id, or use --list-campaigns")
        sys.exit(1)

    print(json.dumps(result, indent=2))
