# pylint: disable=duplicate-code
"""Demonstrate minimal usage of :class:`FireflyClient`. editing notes"""

import os
import logging

from dotenv import load_dotenv
from fireflyiii_enricher_core.firefly_client import FireflyClient

logging.basicConfig(
    level=logging.INFO,  # lub DEBUG
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

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

TX_ID = 3896
firefly.update_transaction_notes(TX_ID, "Test notes#1\nTest notes#3")
