#!/usr/bin/env python3
"""
Recipe: credit-balance
Add money to player via Wallet API (fastest) or BackOffice API (safer).
Returns: success status, new balance
"""

import json
import random
import string
import sys

import requests

from env_config import (
    DEFAULT_BRAND,
    DEFAULT_ENV,
    backoffice_headers,
    get_brand,
    get_env,
)


def _random_tx_id() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=20))


def credit_via_wallet(
    player_id: int,
    amount: float = 100.0,
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
    comment: str = "QA auto credit",
) -> dict:
    """
    Credit player balance via Wallet API (direct, fast).

    Args:
        player_id: Player ID
        amount: Amount to credit
        env: Environment
        brand: Brand name
        comment: Transaction comment

    Returns:
        dict with keys: success, balance, method
    """
    e = get_env(env)
    b = get_brand(brand)

    url = f"{e['wallet_api']}/{b['partner_id']}/api/v1/transaction/correction/debit"

    tx_id = _random_tx_id()
    data = {
        "clientId": player_id,
        "currency": b["currency"],
        "amount": amount,
        "externalTransactionId": tx_id,
        "TransactionId": tx_id,
        "OperationType": "CorrectionDebit",
        "comment": comment,
    }

    resp = requests.post(url, json=data, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Wallet credit failed: {resp.status_code} - {resp.text}")

    # Verify balance
    balance = get_balance(player_id, env=env, brand=brand)

    result = {
        "success": True,
        "player_id": player_id,
        "credited": amount,
        "currency": b["currency"],
        "balance": balance,
        "method": "wallet",
        "env": env,
    }

    print(f"[credit-balance] player_id={player_id} +{amount} {b['currency']} via wallet env={env}")
    return result


def credit_via_backoffice(
    player_id: int,
    amount: float = 100.0,
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
    comment: str = "QA auto credit",
) -> dict:
    """
    Credit player balance via BackOffice API (admin path, safer).

    Args:
        player_id: Player ID
        amount: Amount to credit
        env: Environment
        brand: Brand name
        comment: Transaction comment

    Returns:
        dict with keys: success, balance, method
    """
    e = get_env(env)
    b = get_brand(brand)

    url = f"{e['backoffice_api']}/api/Client/CreateDebitCorrection"

    data = {
        "clientId": player_id,
        "amount": amount,
        "currency": b["currency"],
        "externalTransactionId": _random_tx_id(),
        "comment": comment,
        "isTest": True,
    }

    resp = requests.post(url, headers=backoffice_headers(env), json=data, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"BO credit failed: {resp.status_code} - {resp.text}")

    # Verify balance
    balance = get_balance(player_id, env=env, brand=brand)

    result = {
        "success": True,
        "player_id": player_id,
        "credited": amount,
        "currency": b["currency"],
        "balance": balance,
        "method": "backoffice",
        "env": env,
    }

    print(f"[credit-balance] player_id={player_id} +{amount} {b['currency']} via backoffice env={env}")
    return result


def get_balance(
    player_id: int,
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
) -> dict:
    """Get player balance from Wallet API."""
    e = get_env(env)
    b = get_brand(brand)

    url = f"{e['wallet_api']}/{b['partner_id']}/api/v1/balance/{player_id}/{b['currency']}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        return resp.json()
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Credit player balance")
    parser.add_argument("--player-id", required=True, type=int)
    parser.add_argument("--amount", default=100.0, type=float)
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--brand", default=DEFAULT_BRAND)
    parser.add_argument("--method", default="wallet", choices=["wallet", "backoffice"])
    args = parser.parse_args()

    if args.method == "wallet":
        result = credit_via_wallet(args.player_id, args.amount, args.env, args.brand)
    else:
        result = credit_via_backoffice(args.player_id, args.amount, args.env, args.brand)
    print(json.dumps(result, indent=2))
