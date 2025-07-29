"""Demonstrate minimal usage of :class:`FireflyClient`. editing notes"""

import json
import os

from dotenv import load_dotenv

from fireflyiii_enricher_core.firefly_client import FireflyClient

# Load environment variables from .env.example file
load_dotenv()

FIREFLY_URL = os.getenv("FIREFLY_URL")
FIREFLY_TOKEN = os.getenv("FIREFLY_TOKEN")

if FIREFLY_URL is None or FIREFLY_TOKEN is None:
    raise RuntimeError("Missing FIREFLY_URL or FIREFLY_TOKEN in environment. ")

# Initialize Firefly III client with credentials
firefly = FireflyClient(base_url=FIREFLY_URL, token=FIREFLY_TOKEN)

TX_ID = 3896
response = firefly.add_tag_to_transaction(TX_ID, "test tag#3")


print(json.dumps(response, indent=2, ensure_ascii=False))
