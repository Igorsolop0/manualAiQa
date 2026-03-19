#!/usr/bin/env python3
"""
Recipe: login-player
Login an existing player and return a fresh session token.
Returns: session_token, balance
"""

import json
import sys

import requests

from env_config import (
    DEFAULT_BRAND,
    DEFAULT_ENV,
    DEFAULT_PASSWORD,
    get_brand,
    get_env,
    website_headers,
)


def login_player(
    email: str,
    password: str = DEFAULT_PASSWORD,
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
) -> dict:
    """
    Login player via Website REST API.

    Args:
        email: Player email
        password: Player password
        env: Environment
        brand: Brand name

    Returns:
        dict with keys: session_token, player_id, balance
    """
    e = get_env(env)
    b = get_brand(brand)

    url = f"{e['website_api']}/{b['partner_id']}/api/v3/Client/Login"

    headers = website_headers(env)
    data = {
        "email": email,
        "password": password,
        "partnerId": b["partner_id"],
        "deviceType": 1,  # Desktop
    }

    resp = requests.post(url, json=data, headers=headers, timeout=30)
    resp.raise_for_status()

    result = resp.json()
    if result.get("ResponseCode") != "Success":
        raise RuntimeError(
            f"Login failed: {result.get('Description', 'Unknown error')}"
        )

    token = result.get("ResponseObject", {}).get("Token")
    player_id = result.get("ResponseObject", {}).get("Id")
    if not token:
        raise RuntimeError("No token in response")

    # Get balance
    balance = None
    try:
        bal_url = f"{e['website_api']}/{b['partner_id']}/api/v3/Client/GetClientBalance"
        bal_headers = {**headers, "Authorization": token}
        bal_resp = requests.get(bal_url, headers=bal_headers, timeout=15)
        if bal_resp.status_code == 200:
            balance = bal_resp.json()
    except Exception:
        pass  # balance is optional

    login_result = {
        "session_token": token,
        "player_id": player_id,
        "email": email,
        "balance": balance,
        "brand": brand,
        "env": env,
    }

    print(f"[login-player] player_id={player_id} email={email} env={env}")
    return login_result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Login a player")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--brand", default=DEFAULT_BRAND)
    args = parser.parse_args()

    result = login_player(
        email=args.email, password=args.password, env=args.env, brand=args.brand
    )
    print(json.dumps(result, indent=2))
