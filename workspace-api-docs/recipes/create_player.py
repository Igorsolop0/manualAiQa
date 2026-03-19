#!/usr/bin/env python3
"""
Recipe: create-player
Create a test player via Website GraphQL API.
Returns: player_id, email, password, session_token
"""

import json
import random
import sys
import time

import requests

from env_config import (
    DEFAULT_BRAND,
    DEFAULT_ENV,
    DEFAULT_PASSWORD,
    get_brand,
    get_env,
    website_headers,
)


def create_player(
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
    email: str = None,
    password: str = DEFAULT_PASSWORD,
    prefix: str = "qa-auto",
) -> dict:
    """
    Register a new test player.

    Args:
        env: Environment (qa, prod)
        brand: Brand name (minebit, turabet, etc.)
        email: Custom email (auto-generated if None)
        password: Player password
        prefix: Email prefix for identification

    Returns:
        dict with keys: player_id, email, password, session_token, username
    """
    e = get_env(env)
    b = get_brand(brand)

    if email is None:
        ts = int(time.time() * 1000)
        suffix = random.randint(1000, 9999)
        email = f"{prefix}-{ts}-{suffix}@nextcode.tech"

    mutation = """
    mutation PlayerRegisterUniversal(
        $input: PlayerRegisterUniversalInput!
        $bmsPartnerId: Int!
        $locale: Locale!
        $deviceFingerPrint: String
    ) {
        playerRegisterUniversal(
            input: $input
            bmsPartnerId: $bmsPartnerId
            locale: $locale
            deviceFingerPrint: $deviceFingerPrint
        ) {
            record {
                sessionToken
                userName
                id
                email
            }
            status
        }
    }
    """

    variables = {
        "input": {
            "email": email,
            "password": password,
            "currency": b["currency"],
            "promoCode": None,
            "termsConditionsAccepted": True,
            "affiliateData": e["site_origin"],
        },
        "bmsPartnerId": b["partner_id"],
        "locale": "en",
        "deviceFingerPrint": "".join(
            [str(random.randint(0, 9)) for _ in range(32)]
        ),
    }

    payload = {
        "operationName": "PlayerRegisterUniversal",
        "variables": variables,
        "query": mutation,
    }

    resp = requests.post(
        e["graphql"], headers=website_headers(env), json=payload, timeout=30
    )

    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}")

    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")

    record = (
        data.get("data", {})
        .get("playerRegisterUniversal", {})
        .get("record")
    )
    if not record:
        raise RuntimeError(f"No record returned: {data}")

    result = {
        "player_id": record["id"],
        "email": email,
        "password": password,
        "session_token": record["sessionToken"],
        "username": record.get("userName", ""),
        "brand": brand,
        "env": env,
    }

    print(f"[create-player] player_id={result['player_id']} email={email} env={env} brand={brand}")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a test player")
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--brand", default=DEFAULT_BRAND)
    parser.add_argument("--email", default=None)
    parser.add_argument("--prefix", default="qa-auto")
    args = parser.parse_args()

    result = create_player(env=args.env, brand=args.brand, email=args.email, prefix=args.prefix)
    print(json.dumps(result, indent=2))
