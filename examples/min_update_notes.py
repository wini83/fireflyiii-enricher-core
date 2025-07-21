# pylint: disable=duplicate-code
"""Demonstrate minimal usage of :class:`FireflyClient`. editing notes"""

import json
import os

from dotenv import load_dotenv

from fireflyiii_enricher_core.firefly_client import FireflyClient

# Load environment variables from .env.example file
load_dotenv()

# Initialize Firefly III client with demo credentials
firefly = FireflyClient(
    base_url=os.getenv("FIREFLY_URL"), token=os.getenv('FIREFLY_TOKEN')
)

TX_ID = 3896
response = firefly.update_transaction_notes(TX_ID, "Test notes#5\nTest notes#6")
print(json.dumps(response, indent=2, ensure_ascii=False))
