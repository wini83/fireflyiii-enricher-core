# pylint: disable=duplicate-code
"""Demonstrate minimal usage of :class:`FireflyClient`. editing notes"""

import os
import json

from dotenv import load_dotenv
from fireflyiii_enricher_core.firefly_client import FireflyClient

# Load environment variables from .env.example file
load_dotenv()

# Initialize Firefly III client with demo credentials
firefly = FireflyClient(
    base_url=os.getenv("FIREFLY_URL"),
    token=os.getenv('FIREFLY_TOKEN')
)

TX_ID = 3896
response =  firefly.update_transaction_description(TX_ID, "BLIK - płatność w internecie")
print(json.dumps(response, indent=2, ensure_ascii=False))
