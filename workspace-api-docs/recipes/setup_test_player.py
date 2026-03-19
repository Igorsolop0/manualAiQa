#!/usr/bin/env python3
"""
Recipe: setup-test-player
Composite recipe: create player + credit balance in one call.
This is the most common data prep operation for QA tasks.
Returns: full player context ready for testing
"""

import json
import sys

from env_config import DEFAULT_BRAND, DEFAULT_ENV

from create_player import create_player
from credit_balance import credit_via_wallet, credit_via_backoffice


def setup_test_player(
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
    balance: float = 100.0,
    prefix: str = "qa-auto",
) -> dict:
    """
    Create a new test player with balance, ready for testing.

    Args:
        env: Environment
        brand: Brand name
        balance: Starting balance to credit
        prefix: Email prefix

    Returns:
        dict with all player info + balance
    """
    # Step 1: Register player
    player = create_player(env=env, brand=brand, prefix=prefix)
    print(f"[setup-test-player] step 1/2: player created")

    # Step 2: Credit balance (try wallet first, fallback to backoffice)
    try:
        credit = credit_via_wallet(
            player_id=player["player_id"],
            amount=balance,
            env=env,
            brand=brand,
            comment=f"Initial balance for {prefix}",
        )
    except RuntimeError as e:
        print(f"[setup-test-player] wallet credit failed ({e}), trying backoffice...")
        credit = credit_via_backoffice(
            player_id=player["player_id"],
            amount=balance,
            env=env,
            brand=brand,
            comment=f"Initial balance for {prefix}",
        )
    print(f"[setup-test-player] step 2/2: balance credited")

    result = {
        **player,
        "initial_balance": balance,
        "wallet_balance": credit.get("balance"),
        "ready": True,
    }

    print(f"[setup-test-player] READY: player_id={result['player_id']} balance={balance} env={env}")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create player with balance")
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--brand", default=DEFAULT_BRAND)
    parser.add_argument("--balance", default=100.0, type=float)
    parser.add_argument("--prefix", default="qa-auto")
    args = parser.parse_args()

    result = setup_test_player(
        env=args.env, brand=args.brand, balance=args.balance, prefix=args.prefix
    )
    print(json.dumps(result, indent=2))
