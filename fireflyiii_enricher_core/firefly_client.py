"""Moduł do obsługi Firefly III API."""
import requests
import logging

logger = logging.getLogger(__name__)


class FireflyClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def fetch_transactions(self, tx_type="withdrawal", limit=1000):
        logger.info("Pobieranie transakcji typu '%s' z Firefly...", tx_type)
        url = f"{self.base_url}/api/v1/transactions"
        params = {"limit": limit, "type": tx_type}
        page = 1
        transactions = []

        while True:
            params["page"] = page
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            transactions.extend(data["data"])

            if not data["links"].get("next"):
                break
            page += 1

        return transactions

    def filter_single_part(self, transactions):
        return [
            t for t in transactions if len(t["attributes"]["transactions"]) == 1
        ]

    def filter_without_category(self, transactions):
        return [
            t for t in transactions
            if t["attributes"]["transactions"][0].get("relationships", {})
            .get("category", {}).get("data") is None
        ]

    def filter_by_description(self, transactions, description_filter, exact_match=True):
        filtered = []
        for t in transactions:
            desc = t["attributes"]["transactions"][0]["description"]
            if exact_match and desc.lower() == description_filter.lower():
                filtered.append(t)
            elif not exact_match and description_filter.lower() in desc.lower():
                filtered.append(t)
        return filtered

    def simplify_transactions(self, transactions):
        return [{
            "id": t["id"],
            "description": t["attributes"]["transactions"][0]["description"],
            "amount": t["attributes"]["transactions"][0]["amount"],
            "date": t["attributes"]["transactions"][0]["date"]
        } for t in transactions]

    def update_transaction_description(self, transaction_id, new_description):
        url = f"{self.base_url}/api/v1/transactions/{transaction_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            logger.error("Nie udało się pobrać transakcji %s", transaction_id)
            return

        payload = {
            "apply_rules": True,
            "fire_webhooks": True,
            "transactions": [{"description": new_description}]
        }

        put_response = requests.put(url, headers=self.headers, json=payload, timeout=10)
        if put_response.status_code == 200:
            logger.info("Zaktualizowano opis transakcji %s", transaction_id)
        else:
            logger.error("Błąd aktualizacji %s: %s - %s",
                         transaction_id, put_response.status_code, put_response.text)
