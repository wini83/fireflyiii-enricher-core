"""Utility client for interacting with the Firefly III API."""

import logging
import requests

logger = logging.getLogger(__name__)

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

    def filter_single_part(self, transactions):
        """Return only transactions that have a single sub-transaction."""
        return [
            t for t in transactions
            if len(t["attributes"]["transactions"]) == 1
        ]

    def filter_without_category(self, transactions):
        """Filter out transactions that already have a category set."""
        return [
            t for t in transactions
            if t["attributes"]["transactions"][0]
               .get("relationships", {}).get("category", {}).get("data") is None
        ]

    def filter_by_description(self, transactions, description_filter, exact_match=True):
        """Match transactions whose description matches the filter."""
        filtered = []
        for t in transactions:
            desc = t["attributes"]["transactions"][0]["description"]
            if exact_match and desc.lower() == description_filter.lower():
                filtered.append(t)
            elif not exact_match and description_filter.lower() in desc.lower():
                filtered.append(t)
        return filtered

    def simplify_transactions(self, transactions):
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

    def update_transaction_description(self, transaction_id, new_description):
        """Change the description field for a given transaction."""
        url = f"{self.base_url}/api/v1/transactions/{transaction_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch transaction {transaction_id}: {e}")
            return

        payload = {
            "apply_rules": True,
            "fire_webhooks": True,
            "transactions": [{"description": new_description}]
        }

        try:
            response = requests.put(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Updated description for transaction {transaction_id}")
        except requests.RequestException as e:
            logger.error(f"Update error for {transaction_id}: {e}")

    def update_transaction_notes(self, transaction_id, new_notes):
        """Replace the notes for a given transaction."""
        url = f"{self.base_url}/api/v1/transactions/{transaction_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to fetch transaction {transaction_id}")
            return
        existing_data = response.json()
        old_description = existing_data.get("data", {}).get("attributes", {}).get("description", "")
        payload = {
            "apply_rules": True,
            "fire_webhooks": True,
            "transactions": [{
                "description": old_description,
                "notes": new_notes
            }]
        }
        response = requests.put(url, headers=self.headers, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info(f"Updated notes for transaction {transaction_id}")
        else:
            logger.error(
                f"Error updating notes for {transaction_id}: {response.status_code} - {response.text}"
            )

    def add_tag_to_transaction(self, transaction_id, tag_id):
        """Attach a tag to the specified transaction."""
        url = f"{self.base_url}/api/v1/transactions/{transaction_id}/tags"
        payload = {"tags": [str(tag_id)]}
        response = requests.post(url, headers=self.headers, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info(f"Added tag {tag_id} to transaction {transaction_id}")
        else:
            logger.error(
                f"Error adding tag {tag_id} to transaction {transaction_id}: {response.status_code} - {response.text}"
            )
