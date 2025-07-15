"""Unit tests for FireflyClient class."""

from unittest.mock import patch
import pytest
import requests
from fireflyiii_enricher_core.firefly_client import FireflyClient

BASE_URL = "https://demo.firefly.local"
TOKEN = "test-token"


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_fetch_transactions(mock_request):
    """Test fetching paginated transactions."""
    mock_request.side_effect = [
        MockResponse({
            "data": [{"id": "1"}, {"id": "2"}],
            "links": {"next": "some_url"}
        }),
        MockResponse({
            "data": [{"id": "3"}],
            "links": {"next": None}
        }),
    ]

    client = FireflyClient(BASE_URL, TOKEN)
    result = client.fetch_transactions()
    assert len(result) == 3


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_update_description_success(mock_request):
    """Test successful update of transaction description."""
    mock_request.return_value = MockResponse({})
    client = FireflyClient(BASE_URL, TOKEN)
    client.update_transaction_description(123, "Test")


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_update_transaction_notes_success(mock_request):
    """Test successful update of transaction notes."""
    mock_request.return_value = MockResponse({})
    client = FireflyClient(BASE_URL, TOKEN)
    client.update_transaction_notes(123, "Some note")


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_add_tag_to_transaction(mock_request):
    """Test successful adding of a tag to a transaction."""
    mock_response_data = {
        "data": {
            "attributes": {
                "transactions": [
                    {
                        "description": "Old description",
                        "tags": []
                    }
                ]
            }
        }
    }
    mock_request.return_value = MockResponse(mock_response_data)
    client = FireflyClient(BASE_URL, TOKEN)
    client.add_tag_to_transaction(123, "processed")



@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_timeout_handling(mock_request):
    """Test timeout exception is handled and re-raised."""
    mock_request.side_effect = requests.Timeout()
    client = FireflyClient(BASE_URL, TOKEN)
    with pytest.raises(RuntimeError, match="Request timed out"):
        client.fetch_transactions()


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_json_decode_error(mock_request):
    """Test JSON decode error is handled gracefully."""
    class BadJsonResponse:
        """Mocked response that raises ValueError on json()."""
        def raise_for_status(self):
            """Mocked response that raises ValueError on json()."""
            return

        def json(self):
            """Mocked response that raises ValueError on json()."""
            raise ValueError("bad json")

    mock_request.return_value = BadJsonResponse()
    client = FireflyClient(BASE_URL, TOKEN)
    with pytest.raises(RuntimeError, match="Failed to parse JSON response"):
        client.fetch_transactions()


class MockResponse:
    """Generic mock response for testing purposes."""

    def __init__(self, json_data):
        """Initialize with mock JSON data."""
        self._json = json_data
        self.status_code = 200

    def json(self):
        """Return mocked JSON content."""
        return self._json

    def raise_for_status(self):
        """Simulate successful response (does nothing)."""
        # No action needed for success simulation
        return
