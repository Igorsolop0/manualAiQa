"""
Shared environment configuration for all recipes.
Single source of truth for URLs, credentials, and brand settings.
"""

ENVIRONMENTS = {
    "qa": {
        "graphql": "https://minebit-casino.qa.sofon.one/graphql",
        "website_api": "https://websitewebapi.qa.sofon.one",
        "backoffice_api": "https://adminwebapi.qa.sofon.one",
        "wallet_api": "https://wallet.qa.sofon.one",
        "crm_gateway": "https://crmgateway.qa.sofon.one",
        "site_origin": "https://minebit-casino.qa.sofon.one",
        "bo_user_id": "1",
    },
    "prod": {
        "graphql": "https://minebit.io/graphql",
        "website_api": "https://websitewebapi.prod.sofon.one",
        "backoffice_api": "https://adminwebapi.prod.sofon.one",
        "wallet_api": "https://wallet.prod.sofon.one",
        "crm_gateway": "https://crmgateway.prod.sofon.one",
        "site_origin": "https://minebit.io",
        "bo_user_id": "560",
    },
}

BRANDS = {
    "minebit": {"partner_id": 5, "currency": "USD"},
    "turabet": {"partner_id": 8, "currency": "TRY"},
    "betazo": {"partner_id": 10, "currency": "BRL"},
    "motor": {"partner_id": 12, "currency": "USD"},
}

DEFAULT_PASSWORD = "Qweasd123!"
DEFAULT_ENV = "qa"
DEFAULT_BRAND = "minebit"


def get_env(env: str = DEFAULT_ENV) -> dict:
    """Get environment config. Raises KeyError if env not found."""
    return ENVIRONMENTS[env]


def get_brand(brand: str = DEFAULT_BRAND) -> dict:
    """Get brand config. Raises KeyError if brand not found."""
    return BRANDS[brand]


def website_headers(env: str = DEFAULT_ENV) -> dict:
    """Standard headers for Website API / GraphQL requests."""
    e = get_env(env)
    return {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": e["site_origin"],
        "Referer": f"{e['site_origin']}/",
        "website-locale": "en",
        "website-origin": e["site_origin"],
        "x-time-zone-offset": "-60",
    }


def backoffice_headers(env: str = DEFAULT_ENV) -> dict:
    """Standard headers for BackOffice API requests."""
    e = get_env(env)
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "UserId": e["bo_user_id"],
    }


# Smartico CRM Gateway credentials (shared across environments)
CRM_API_USER_ID = "560"
CRM_API_KEY = "ihorsnextcodebo"


def crm_headers() -> dict:
    """Standard headers for CRM Gateway (Smartico) API requests."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Api-UserId": CRM_API_USER_ID,
        "Api-Key": CRM_API_KEY,
    }
