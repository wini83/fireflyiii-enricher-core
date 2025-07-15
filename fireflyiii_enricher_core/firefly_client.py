"""Utility client for interacting with the Firefly III API."""

import logging
import requests

logger = logging.getLogger(__name__)


def filter_single_part(transactions):
    """Return only transactions that have a single sub-transaction."""
    return [
        t for t in transactions
        if len(t["attributes"]["transactions"]) == 1
    ]


def filter_without_category(transactions):
    """Filter out transactions that already have a category set."""
    return [
        t for t in transactions
        if t["attributes"]["transactions"][0]
           .get("relationships", {}).get("category", {}).get("data") is None
    ]


def filter_by_description(transactions, description_filter:str, exact_match:bool=True):
    """Match transactions whose description matches the filter."""
    filtered = []
    for t in transactions:
        desc = t["attributes"]["transactions"][0]["description"]
        if exact_match and desc.lower() == description_filter.lower():
            filtered.append(t)
        elif not exact_match and description_filter.lower() in desc.lower():
            filtered.append(t)
    return filtered


def simplify_transactions(transactions):
    """Convert the raw API response into a flat structure."""
    simplified = []
    for t in transactions:
        sub = t["attributes"]["transactions"][0]
        simplified.append({
            "id": t["id"],
            "description": sub["description"],
            "amount": sub["amount"],
            "date": sub["date"]
        })
    return simplified


class FireflyClient:
    """Minimal wrapper around the Firefly III REST API."""

    def __init__(self, base_url, headers):
        """Store connection details for later requests."""
        self.base_url = base_url
        self.headers = headers

    def fetch_transactions(self, tx_type="withdrawal", limit=1000):
        """Retrieve transactions of the given type."""
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

    def update_transaction_description(self, transaction_id: int, new_description:str):
        """Change the description field for a given transaction."""
        url = f"{self.base_url}/api/v1/transactions/{transaction_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as err:
            logger.error(
                "Failed to fetch transaction %s: %s", transaction_id, err
            )
            return

        payload = {
            "apply_rules": True,
            "fire_webhooks": True,
            "transactions": [{"description": new_description}]
        }

        try:
            response = requests.put(
                url, headers=self.headers, json=payload, timeout=10
            )
            response.raise_for_status()
            logger.info(
                "Updated description for transaction %s", transaction_id
            )
        except requests.RequestException as err:
            logger.error("Update error for %s: %s", transaction_id, err)

    def update_transaction_notes(self, transaction_id:int, new_notes:str):
        """Replace the notes for a given transaction."""
        url = f"{self.base_url}/api/v1/transactions/{transaction_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            logger.error(
                "Failed to fetch transaction %s", transaction_id
            )
            return
        payload = {
            "apply_rules": True,
            "fire_webhooks": True,
            "transactions": [{
                "notes": new_notes
            }]
        }
        response = requests.put(
            url, headers=self.headers, json=payload, timeout=10
        )
        if response.status_code == 200:
            logger.info(
                "Updated notes for transaction %s", transaction_id
            )
        else:
            logger.error(
                "Error updating notes for %s: %s - %s",
                transaction_id,
                response.status_code,
                response.text,
            )

    def add_tag_to_transaction(self, transaction_id:int, new_tag:str):
        """Attach a tag to the specified transaction."""

        url = f"{self.base_url}/api/v1/transactions/{transaction_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            logger.error(
                "Failed to fetch transaction %s", transaction_id
            )
            return
        existing_data = response.json()
        old_sub_transactions = (existing_data.get("data", {})
                                .get("attributes", {})
                                .get("transactions", []))
        if len(old_sub_transactions) != 1:
            logger.error(
                "Transaction %s is no single part", transaction_id
            )
            return
        old_sub_tx = old_sub_transactions[0]
        tags = old_sub_tx.get("tags", [])
        tags.append(new_tag)
        payload = {
            "apply_rules": True,
            "fire_webhooks": True,
            "transactions": [{
                "tags": tags
            }]
        }
        response = requests.put(
            url, headers=self.headers, json=payload, timeout=10
        )
        if response.status_code == 200:
            logger.info(
                "Updated tags for transaction %s", transaction_id
            )
        else:
            logger.error(
                "Error updating tags for %s: %s - %s",
                transaction_id,
                response.status_code,
                response.text,
            )
