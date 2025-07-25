# pylint: disable=duplicate-code
"""Demonstrate minimal usage of :class:`FireflyClient`."""

import os

from dotenv import load_dotenv

from fireflyiii_enricher_core.firefly_client import (
    FireflyClient,
    filter_by_description,
    filter_single_part,
    filter_without_tag,
    simplify_transactions,
)

# Load environment variables from .env.example file
load_dotenv()

FIREFLY_URL = os.getenv("FIREFLY_URL")
FIREFLY_TOKEN = os.getenv("FIREFLY_TOKEN")

if FIREFLY_URL is None or FIREFLY_TOKEN is None:
    raise RuntimeError("Missing FIREFLY_URL or FIREFLY_TOKEN in environment.")

# Initialize Firefly III client with credentials
firefly = FireflyClient(base_url=FIREFLY_URL, token=FIREFLY_TOKEN)

# Fetch, filter and simplify transactions
transactions = firefly.fetch_transactions()
transactions = filter_single_part(transactions)
transactions = filter_by_description(transactions, "allegro", exact_match=False)

allegro_not_processed = filter_without_tag(transactions, "allegro_done")
simplified = simplify_transactions(allegro_not_processed)

print(
    f"Transaction allegro: {len(transactions)} -"
    f" not processed {len(allegro_not_processed)}"
)


# Display matching transactions
for tx in simplified:
    print(f"{tx.id}: {tx.date} | {tx.amount} | {tx.description} |{tx.tags}")
