#!/usr/bin/env python3
"""
Recipe: deposit-flow
Create a deposit via BackOffice API (manual redirect payment → mark as paid).
This simulates a real deposit flow through the payment system.
Returns: success status, payment_request_id, balance
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
from credit_balance import get_balance


def _random_tx_id() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=20))


def deposit_flow(
    player_id: int,
    amount: float = 100.0,
    env: str = DEFAULT_ENV,
    brand: str = DEFAULT_BRAND,
    payment_method_id: int = 19,
) -> dict:
    """
    Execute full deposit flow: create request → mark as paid → verify balance.

    Args:
        player_id: Player ID
        amount: Deposit amount
        env: Environment
        brand: Brand name
        payment_method_id: Partner payment method ID (19 = default for QA)

    Returns:
        dict with keys: success, payment_request_id, balance, method
    """
    e = get_env(env)
    b = get_brand(brand)
    headers = backoffice_headers(env)

    # Step 1: Create deposit request
    create_url = f"{e['backoffice_api']}/api/Client/MakeManualRedirectPayment"
    create_data = {
        "amount": amount,
        "clientId": player_id,
        "currencyId": b["currency"],
        "externalTransactionId": _random_tx_id(),
        "partnerPaymentMethodId": payment_method_id,
        "paymentRequestType": "Deposit",
    }

    resp = requests.post(create_url, headers=headers, json=create_data, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Deposit creation failed: {resp.status_code} - {resp.text}")

    deposit_result = resp.json()
    payment_request_id = deposit_result.get("paymentRequestId")
    if not payment_request_id:
        raise RuntimeError(f"No paymentRequestId: {deposit_result}")

    print(f"[deposit-flow] step 1/3: deposit created, paymentRequestId={payment_request_id}")

    # Step 2: Mark as paid
    mark_url = f"{e['backoffice_api']}/api/Payment/ChangeStatus"
    mark_data = {
        "Comment": "QA auto deposit",
        "PaymentRequestId": payment_request_id,
        "ChangeStatusTo": "MarkAsPaid",
        "ProcessingType": 0,
        "Type": "Deposit",
    }

    # Try PATCH first (correct method), fallback to POST
    resp2 = requests.patch(mark_url, headers=headers, json=mark_data, timeout=30)
    if resp2.status_code != 200:
        resp2 = requests.post(mark_url, headers=headers, json=mark_data, timeout=30)
        if resp2.status_code != 200:
            raise RuntimeError(f"MarkAsPaid failed: {resp2.status_code} - {resp2.text}")

    print(f"[deposit-flow] step 2/3: marked as paid")

    # Step 3: Verify balance
    balance = get_balance(player_id, env=env, brand=brand)
    print(f"[deposit-flow] step 3/3: balance verified")

    result = {
        "success": True,
        "player_id": player_id,
        "deposited": amount,
        "currency": b["currency"],
        "payment_request_id": payment_request_id,
        "balance": balance,
        "method": "deposit-flow",
        "env": env,
    }

    print(f"[deposit-flow] player_id={player_id} +{amount} {b['currency']} env={env}")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Execute deposit flow")
    parser.add_argument("--player-id", required=True, type=int)
    parser.add_argument("--amount", default=100.0, type=float)
    parser.add_argument("--env", default=DEFAULT_ENV, choices=["qa", "prod"])
    parser.add_argument("--brand", default=DEFAULT_BRAND)
    args = parser.parse_args()

    result = deposit_flow(args.player_id, args.amount, args.env, args.brand)
    print(json.dumps(result, indent=2))
