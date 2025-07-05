from fireflyiii_enricher_core.firefly_client import FireflyClient
import os
from dotenv import load_dotenv

# Load environment variables from .env.example file
load_dotenv()

# Initialize Firefly III client with demo credentials
firefly = FireflyClient(
    base_url=os.getenv("FIREFLY_URL"),
    headers={
        "Authorization": f"Bearer {os.getenv('FIREFLY_TOKEN')}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json"
    }
)

# Fetch, filter and simplify transactions
transactions = firefly.fetch_transactions()
transactions = firefly.filter_single_part(transactions)
transactions = firefly.filter_by_description(transactions, "allegro", exact_match=False)
simplified = firefly.simplify_transactions(transactions)

# Display matching transactions
for tx in simplified:
    print(f"{tx['id']}: {tx['date']} | {tx['amount']} | {tx['description']}")
