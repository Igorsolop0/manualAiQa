#!/usr/bin/env python3
"""
API clients for Minebit/NextCode APIs.
Supports Website API v3, BackOffice API v1, Wallet API, and GraphQL.
"""

import requests
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from generate_test_data import generate_email, generate_password, generate_external_transaction_id


class WebsiteApiClient:
    """Client for Website API v3 (client-facing API)."""
    
    def __init__(self, base_url: str, partner_id: int, session_token: str = None):
        """
        Initialize Website API client.
        
        Args:
            base_url: Base URL (e.g., https://websitewebapi.qa.sofon.one)
            partner_id: Partner ID (5 for Minebit)
            session_token: Optional session token for authenticated requests
        """
        self.base_url = base_url.rstrip("/")
        self.partner_id = partner_id
        self.session_token = session_token
        
        # Common headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "website-locale": "en",
            "website-origin": "https://minebit-casino.qa.sofon.one",  # Will be updated per env
            "x-time-zone-offset": "-60",
        }
        
        if session_token:
            self.headers["Authorization"] = session_token
    
    def set_session_token(self, token: str):
        """Set session token for authenticated requests."""
        self.session_token = token
        self.headers["Authorization"] = token
    
    def register_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new client via Website API.
        
        Args:
            client_data: Client registration data
            
        Returns:
            Registration response
        """
        url = f"{self.base_url}/{self.partner_id}/api/v3/Client/Register"
        
        # Ensure required fields
        data = client_data.copy()
        if "partnerId" not in data:
            data["partnerId"] = self.partner_id
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Check for success
        if result.get("ResponseCode") != "Success":
            raise Exception(f"Registration failed: {result.get('Description', 'Unknown error')}")
        
        # Extract session token from response
        if "ResponseObject" in result and "Token" in result["ResponseObject"]:
            self.set_session_token(result["ResponseObject"]["Token"])
        
        return result
    
    def get_client_balance(self) -> Dict[str, Any]:
        """
        Get client balance.
        
        Returns:
            Balance response
        """
        url = f"{self.base_url}/{self.partner_id}/api/v3/Client/GetClientBalance"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login client via Website API.
        
        Args:
            email: Client email
            password: Client password
            
        Returns:
            Login response with session token
        """
        url = f"{self.base_url}/{self.partner_id}/api/v3/Client/Login"
        
        data = {
            "partnerId": self.partner_id,
            "email": email,
            "password": password,
            "deviceType": 1,  # Desktop
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ResponseCode") != "Success":
            raise Exception(f"Login failed: {result.get('Description', 'Unknown error')}")
        
        # Extract session token
        if "ResponseObject" in result and "Token" in result["ResponseObject"]:
            self.set_session_token(result["ResponseObject"]["Token"])
        
        return result
    
    def get_games(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get games list.
        
        Args:
            filters: Optional filters
            
        Returns:
            Games list
        """
        url = f"{self.base_url}/{self.partner_id}/api/v3/Product/GetGames"
        
        data = filters or {}
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_active_bonuses(self) -> Dict[str, Any]:
        """
        Get active bonuses for the client.
        
        Returns:
            Active bonuses
        """
        url = f"{self.base_url}/{self.partner_id}/api/v3/Bonus/GetActiveBonuses"
        
        response = requests.post(url, json={}, headers=self.headers)
        response.raise_for_status()
        
        return response.json()


class BackOfficeApiClient:
    """Client for BackOffice API v1 (admin API)."""
    
    def __init__(self, base_url: str, user_id: int):
        """
        Initialize BackOffice API client.
        
        Args:
            base_url: Base URL (e.g., https://adminwebapi.qa.sofon.one)
            user_id: User ID for authentication (1 for QA/Dev, 560 for Prod)
        """
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "UserId": str(user_id),
        }
    
    def get_client_by_id(self, client_id: int) -> Dict[str, Any]:
        """
        Get client details by ID.
        
        Args:
            client_id: Client ID
            
        Returns:
            Client details
        """
        url = f"{self.base_url}/api/Client/GetClientById"
        
        data = {
            "clientId": client_id
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def register_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new client via BackOffice API.
        
        Args:
            client_data: Client registration data
            
        Returns:
            Registration response
        """
        url = f"{self.base_url}/api/Client/RegisterClient"
        
        response = requests.post(url, json=client_data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def change_client_details(self, client_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Change client details (e.g., set IsTest = true).
        
        Args:
            client_id: Client ID
            updates: Fields to update
            
        Returns:
            Update response
        """
        url = f"{self.base_url}/api/Client/ChangeClientDetails"
        
        data = {
            "clientId": client_id,
            **updates
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_manual_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create manual payment (deposit).
        
        Args:
            payment_data: Payment data
            
        Returns:
            Payment creation response
        """
        url = f"{self.base_url}/api/Client/MakeManualRedirectPayment"
        
        response = requests.post(url, json=payment_data, headers=self.headers)
        
        if response.status_code >= 400:
            print(f"❌ Deposit creation failed ({response.status_code})")
            print(f"   URL: {url}")
            print(f"   Request data: {payment_data}")
            print(f"   Response: {response.text}")
            response.raise_for_status()
        
        return response.json()
    
    def change_payment_status(self, payment_request_id: int, status: str = "MarkAsPaid", comment: str = "test") -> Dict[str, Any]:
        """
        Change payment status (e.g., mark deposit as paid).
        
        Args:
            payment_request_id: Payment request ID
            status: New status (MarkAsPaid, Cancel, etc.)
            comment: Comment for the status change
            
        Returns:
            Status change response
        """
        url = f"{self.base_url}/api/Payment/ChangeStatus"
        
        data = {
            "Comment": comment,
            "PaymentRequestId": payment_request_id,
            "ChangeStatusTo": status,
            "ProcessingType": 0,
            "Type": "Deposit"
        }
        
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_bonus_campaign(self, bonus_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create bonus campaign.
        
        Args:
            bonus_data: Bonus campaign data
            
        Returns:
            Creation response
        """
        url = f"{self.base_url}/api/Bonus/CreateCampaign"
        
        response = requests.post(url, json=bonus_data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_client_bonuses(self, client_id: int) -> Dict[str, Any]:
        """
        Get active bonuses for a specific client.
        
        Args:
            client_id: Client ID
            
        Returns:
            Client bonuses
        """
        url = f"{self.base_url}/api/clients/{client_id}/bonuses/active"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()


class WalletApiClient:
    """Client for Wallet API (balance and transactions)."""
    
    def __init__(self, base_url: str, partner_id: int):
        """
        Initialize Wallet API client.
        
        Args:
            base_url: Base URL (e.g., https://wallet.qa.sofon.one)
            partner_id: Partner ID (5 for Minebit)
        """
        self.base_url = base_url.rstrip("/")
        self.partner_id = partner_id
        
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def get_balance(self, client_id: int, currency: str = "USD") -> Dict[str, Any]:
        """
        Get client balance.
        
        Args:
            client_id: Client ID
            currency: Currency code
            
        Returns:
            Balance response
        """
        url = f"{self.base_url}/{self.partner_id}/api/v1/balance/{client_id}/{currency}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_debit_correction(self, client_id: int, amount: float, currency: str = "USD", 
                                reason: str = "test balance setup") -> Dict[str, Any]:
        """
        Create debit correction (ADD money to balance).
        
        IMPORTANT: In Wallet API:
        - CreateDebitCorrection → CREDITS (adds money) ✅
        - CreateCreditCorrection → DEBITS (removes money) ❌
        
        Args:
            client_id: Client ID
            amount: Amount to add
            currency: Currency code
            reason: Reason for correction
            
        Returns:
            Correction response
        """
        url = f"{self.base_url}/{self.partner_id}/api/v1/transaction/correction/debit"
        
        transaction_id = generate_external_transaction_id()
        data = {
            "transactionId": transaction_id,
            "currency": currency,
            "clientId": client_id,
            "partnerId": self.partner_id,
            "amount": amount,
            "operationType": "CorrectionDebit",
            "bonusTurnoverAmount": 0.0,
            "unusedTurnoverAmount": 0.0,
            "rateBalances": None,
            "context": {"reason": reason} if reason else None
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_credit_correction(self, client_id: int, amount: float, currency: str = "USD",
                                 reason: str = "test balance reduction") -> Dict[str, Any]:
        """
        Create credit correction (REMOVE money from balance).
        
        Args:
            client_id: Client ID
            amount: Amount to remove
            currency: Currency code
            reason: Reason for correction
            
        Returns:
            Correction response
        """
        url = f"{self.base_url}/{self.partner_id}/api/v1/transaction/correction/credit"
        
        transaction_id = generate_external_transaction_id()
        data = {
            "transactionId": transaction_id,
            "currency": currency,
            "clientId": client_id,
            "partnerId": self.partner_id,
            "amount": amount,
            "operationType": "CorrectionCredit",
            "bonusTurnoverAmount": 0.0,
            "unusedTurnoverAmount": 0.0,
            "rateBalances": None,
            "context": {"reason": reason} if reason else None
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_transactions(self, client_id: int, limit: int = 10) -> Dict[str, Any]:
        """
        Get client transactions.
        
        Args:
            client_id: Client ID
            limit: Limit of transactions
            
        Returns:
            Transactions list
        """
        url = f"{self.base_url}/{self.partner_id}/api/v1/transaction/list/client/{client_id}?limit={limit}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()


class GraphQLClient:
    """Client for GraphQL API (player registration)."""
    
    def __init__(self, base_url: str):
        """
        Initialize GraphQL client.
        
        Args:
            base_url: Base URL (e.g., https://minebit-casino.qa.sofon.one)
        """
        self.base_url = base_url.rstrip("/")
        
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "website-locale": "en",
            "website-origin": base_url.replace("minebit-casino", "websitewebapi"),  # Derived origin
        }
    
    def register_player(self, email: str, password: str, partner_id: int = 5) -> Dict[str, Any]:
        """
        Register player via GraphQL mutation.
        
        Args:
            email: Player email
            password: Player password
            partner_id: Partner ID (5 for Minebit)
            
        Returns:
            Registration response with session token
        """
        url = f"{self.base_url}/graphql"
        
        # Extract username from email
        username = email.split("@")[0]
        
        mutation = """
        mutation PlayerRegisterUniversal(
          $partnerId: Int!,
          $userName: String!,
          $email: String!,
          $password: String!,
          $firstName: String!,
          $lastName: String!,
          $currencyId: String!,
          $countryCode: String!,
          $countryId: Int!,
          $timeZone: Int!,
          $languageId: String!,
          $termsConditionsAccepted: Boolean!,
          $sendPromotions: Boolean!,
          $sendSms: Boolean!,
          $sendMail: Boolean!,
          $deviceType: Int!
        ) {
          playerRegisterUniversal(
            partnerId: $partnerId,
            userName: $userName,
            email: $email,
            password: $password,
            firstName: $firstName,
            lastName: $lastName,
            currencyId: $currencyId,
            countryCode: $countryCode,
            countryId: $countryId,
            timeZone: $timeZone,
            languageId: $languageId,
            termsConditionsAccepted: $termsConditionsAccepted,
            sendPromotions: $sendPromotions,
            sendSms: $sendSms,
            sendMail: $sendMail,
            deviceType: $deviceType
          ) {
            id
            userName
            email
            token
            state
            __typename
          }
        }
        """
        
        variables = {
            "partnerId": partner_id,
            "userName": username,
            "email": email,
            "password": password,
            "firstName": "Test",
            "lastName": "User",
            "currencyId": "USD",
            "countryCode": "US",
            "countryId": 1,
            "timeZone": 1,
            "languageId": "en",
            "termsConditionsAccepted": True,
            "sendPromotions": False,
            "sendSms": False,
            "sendMail": False,
            "deviceType": 1,
        }
        
        data = {
            "query": mutation,
            "variables": variables
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Check for errors
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
        
        return result


class ApiClientFactory:
    """Factory to create API clients for different environments."""
    
    @staticmethod
    def create_clients(env: str = "qa") -> Dict[str, Any]:
        """
        Create all API clients for specified environment.
        
        Args:
            env: Environment (dev, qa, prod)
            
        Returns:
            Dictionary with all clients
        """
        from generate_test_data import load_config
        config = load_config(env)
        
        # Update website-origin based on environment
        website_origin = f"https://minebit-casino.{env}.sofon.one"
        graphql_url = f"https://minebit-casino.{env}.sofon.one"
        
        clients = {
            "website": WebsiteApiClient(
                base_url=config["website_api"],
                partner_id=config["partner_id"]
            ),
            "backoffice": BackOfficeApiClient(
                base_url=config["backoffice_api"],
                user_id=config["user_id"]
            ),
            "wallet": WalletApiClient(
                base_url=config["wallet_api"],
                partner_id=config["partner_id"]
            ),
            "graphql": GraphQLClient(
                base_url=graphql_url
            ),
            "config": config
        }
        
        # Update website origin header
        clients["website"].headers["website-origin"] = website_origin
        
        return clients


if __name__ == "__main__":
    # Test the API clients
    print("🧪 API Clients Test")
    print("=" * 50)
    
    try:
        clients = ApiClientFactory.create_clients("qa")
        print(f"✅ Created clients for QA environment")
        print(f"   Website API: {clients['website'].base_url}")
        print(f"   BackOffice API: {clients['backoffice'].base_url}")
        print(f"   Wallet API: {clients['wallet'].base_url}")
        print(f"   GraphQL: {clients['graphql'].base_url}")
        print(f"   Partner ID: {clients['config']['partner_id']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")