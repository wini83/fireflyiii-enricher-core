"""Unit tests for :class:`FireflyClient`."""

from unittest.mock import patch

import pytest
import requests

from fireflyiii_enricher_core.firefly_client import FireflyClient

BASE_URL = "https://demo.firefly.local"
HEADERS = {"Authorization": "Bearer test-token"}

def fake_response(status_code=200, json_data=None):
    """Return a minimal fake response object used for mocking."""
    class FakeResponse:
        """Minimal fake response object used for mocking."""
        def __init__(self):
            self.status_code = status_code
            self._json = json_data or {}

        def json(self):
            """Return the fake JSON payload."""
            return self._json

        def raise_for_status(self):
            """Raise an HTTP error if status_code is 400 or above."""
            if self.status_code >= 400:
                raise requests.RequestException("HTTP error")

    return FakeResponse()

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_fetch_transactions(mock_get):
    """Test that transactions are fetched and parsed correctly."""
    mock_get.return_value = fake_response(json_data={
        "data": [{"id": "123", "attributes": {"transactions": [{"description": "test"}]}}],
        "links": {"next": None}
    })

    client = FireflyClient(BASE_URL, HEADERS)
    result = client.fetch_transactions()

    assert len(result) == 1
    assert result[0]["id"] == "123"

@patch("fireflyiii_enricher_core.firefly_client.requests.put")
@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_update_description_success(mock_get, mock_put):
    """Test updating a description successfully."""
    mock_get.return_value = fake_response()
    mock_put.return_value = fake_response()

    client = FireflyClient(BASE_URL, HEADERS)
    client.update_transaction_description(123, "new desc")

    mock_put.assert_called_once()
    _, kwargs = mock_put.call_args
    assert "new desc" in str(kwargs["json"])

@patch("fireflyiii_enricher_core.firefly_client.requests.put")
@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_update_transaction_notes(mock_get, mock_put):
    """Test updating notes on a transaction."""
    mock_get.return_value = fake_response(
        json_data={"data": {"id": "123", "attributes": {"description": "desc"}}}
    )
    mock_put.return_value = fake_response()

    client = FireflyClient(BASE_URL, HEADERS)
    client.update_transaction_notes(123, new_notes="note test")

    mock_put.assert_called_once()
    _, kwargs = mock_put.call_args
    assert kwargs["json"]["transactions"][0]["notes"] == "note test"

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_fetch_transactions_http_error(mock_get):
    """Test handling of HTTP errors while fetching transactions."""
    mock_get.return_value = fake_response(status_code=500)
    client = FireflyClient(BASE_URL, HEADERS)
    with pytest.raises(Exception):
        client.fetch_transactions()

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_update_transaction_description_http_error_on_get(mock_get):
    """Update description when GET request fails should be logged."""
    mock_get.return_value = fake_response(status_code=404)
    client = FireflyClient(BASE_URL, HEADERS)
    # Should not raise, only log the error
    client.update_transaction_description(123, "test")

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
@patch("fireflyiii_enricher_core.firefly_client.requests.put")
def test_update_transaction_description_http_error_on_put(mock_put, mock_get):
    """Update description when PUT request fails should be logged."""
    mock_get.return_value = fake_response()
    mock_put.return_value = fake_response(status_code=500)
    client = FireflyClient(BASE_URL, HEADERS)
    # Should not raise, only log the error
    client.update_transaction_description(123, "test")
