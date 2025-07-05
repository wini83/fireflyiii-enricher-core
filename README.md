# Firefly III Enricher Core

Firefly III Enricher Core is a lightweight library for retrieving and updating
transaction data using the Firefly III API. It also includes tools to match
transactions from Firefly III with records from other sources.

## Features

- Simple `FireflyClient` wrapper around the Firefly III REST API
- `TransactionMatcher` for aligning your bank data with Firefly entries
- Example script demonstrating basic usage
- Pytest based unit tests

## Installation

Clone the repository and install the package in editable mode:

```bash
pip install -e .
```

For development you can install additional dependencies:

```bash
pip install -e .[dev]
```

## Usage

Set up your Firefly III credentials in an environment file and run the example
script:

```bash
python examples/minimal_usage.py
```

The script will fetch transactions from your Firefly III instance and print a
simplified list to the console.

## Running Tests

Use `pytest` to execute the test suite:

```bash
pytest
```

## License

This project is licensed under the MIT License.
