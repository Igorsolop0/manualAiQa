#!/usr/bin/env python3
"""
Recipe: get-bonuses
Retrieve active bonuses from BackOffice API.
Useful for monitoring and pre-test data discovery.
Returns: list of bonuses with key fields
"""

import json
import sys

import requests

from env_config import (
    DEFAULT_BRAND,
    DEFAULT_ENV,
    backoffice_headers,
    get_brand,
    get_env,
)


def get_bonuses(
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
    active_only: bool = True,
    limit: int = 100,
) -> dict:
    """
    Get bonuses from BackOffice API.

    Args:
        env: Environment (qa, prod)
        brand: Brand name
        active_only: Only return active bonuses
        limit: Max bonuses to return

    Returns:
        dict with keys: bonuses (list), total_count, env
    """
    e = get_env(env)
    b = get_brand(brand)

    url = f"{e['backoffice_api']}/api/Bonus/GetBonuses"
    payload = {
        "partnerId": b["partner_id"],
        "takeCount": limit,
        "skipCount": 0,
        "isActive": active_only,
    }

    resp = requests.post(
        url, json=payload, headers=backoffice_headers(env), timeout=30
    )
    if resp.status_code != 200:
        raise RuntimeError(f"GetBonuses failed: {resp.status_code} - {resp.text}")

    data = resp.json()
    bonuses_raw = data.get("ResponseObject", {}).get("Entities", [])

    # Extract key fields for each bonus
    bonuses = []
    for b_item in bonuses_raw:
        bonuses.append({
            "id": b_item.get("Id"),
            "name": b_item.get("Name"),
            "type": b_item.get("TypeId"),
            "status": "active" if b_item.get("Status") == 1 else "inactive",
            "bet_real_percent": b_item.get("BetRealPercent"),
            "wagering_multiplier": b_item.get("WageringMultiplier"),
            "min_deposit": b_item.get("MinDeposit"),
            "max_bonus": b_item.get("MaxBonusAmount"),
        })

    result = {
        "bonuses": bonuses,
        "total_count": len(bonuses),
        "env": env,
        "brand": brand,
        "active_only": active_only,
    }

    print(f"[get-bonuses] found {len(bonuses)} bonuses on {env}/{brand}")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get bonuses inventory")
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--brand", default=DEFAULT_BRAND)
    parser.add_argument("--all", action="store_true", help="Include inactive bonuses")
    args = parser.parse_args()

    result = get_bonuses(env=args.env, brand=args.brand, active_only=not args.all)
    print(json.dumps(result, indent=2))
