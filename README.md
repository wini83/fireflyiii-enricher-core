# Firefly III Enricher Core 
[![Python package](https://github.com/wini83/fireflyiii-enricher-core/actions/workflows/python-package.yml/badge.svg)](https://github.com/wini83/fireflyiii-enricher-core/actions/workflows/python-package.yml) [![Pylint](https://github.com/wini83/fireflyiii-enricher-core/actions/workflows/pylint.yml/badge.svg)](https://github.com/wini83/fireflyiii-enricher-core/actions/workflows/pylint.yml)

A Python library for enriching Firefly III transactions by updating descriptions, notes, and tags.

## ✨ Features

- ✅ Fetch transactions from Firefly III API
- 📝 Update transaction **descriptions** and **notes**
- 🏷️ Add tags to transactions
- 🚫 Filter uncategorized or single-part transactions
- ⚠️ Robust error handling (timeouts, connection issues, malformed responses)

## 📦 Installation

```bash
pip install git+https://github.com/wini83/fireflyiii-enricher-core.git
```

## 🧰 Requirements

- Python 3.8+
- `requests`
- `python-dotenv` (optional, for loading environment variables from `.env`)

## ⚙️ Usage

### Environment Setup

```env
# .env file
FIREFLY_URL=https://your-firefly-instance/api
FIREFLY_TOKEN=your_access_token
```

### Minimal Example

```python
from fireflyiii_enricher_core.firefly_client import FireflyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = FireflyClient(
    base_url=os.getenv("FIREFLY_URL"),
    token=os.getenv("FIREFLY_TOKEN")
)

# Fetch latest withdrawals
transactions = client.fetch_transactions()

# Update description
client.update_transaction_description("123", "New description")

# Update notes
client.update_transaction_notes("123", "Some extra notes")

# Add a tag
client.add_tag_to_transaction("123", "processed")
```

## 🧪 Testing

### Install development dependencies

```bash
pip install -e .[dev]
```

### Run tests

```bash
pytest
```

### Linting

```bash
pylint $(git ls-files '*.py')
```

## 🛠 Development

- Use `.env` for secrets/tokens (not committed to version control)
- Follow PEP8 and naming conventions
- Keep public methods well-documented

## 📄 License

MIT License — see [`LICENSE`](LICENSE) for full text.
