# pylint: disable=duplicate-code
"""Demonstrate minimal usage of :class:`FireflyClient`."""

import os
from dotenv import load_dotenv
from fireflyiii_enricher_core.firefly_client import (FireflyClient,
                                                     filter_single_part,
                                                     filter_by_description,
                                                     simplify_transactions)

# Load environment variables from .env.example file
load_dotenv()

# Initialize Firefly III client with demo credentials
firefly = FireflyClient(
    base_url=os.getenv("FIREFLY_URL"),
    token=os.getenv('FIREFLY_TOKEN')
)

# Fetch, filter and simplify transactions
transactions = firefly.fetch_transactions()
transactions = filter_single_part(transactions)
transactions = filter_by_description(transactions, "allegro", exact_match=False)
simplified = simplify_transactions(transactions)

# Display matching transactions
for tx in simplified:
    print(f"{tx['id']}: {tx['date']} | {tx['amount']} | {tx['description']} |{tx['tags']}")
