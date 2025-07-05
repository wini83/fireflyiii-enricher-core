import pytest
import requests

from fireflyiii_enricher_core.firefly_client import FireflyClient
from unittest.mock import patch

BASE_URL = "https://demo.firefly.local"
HEADERS = {"Authorization": "Bearer test-token"}

def fake_response(status_code=200, json_data=None):
    class FakeResponse:
        def __init__(self):
            self.status_code = status_code
            self._json = json_data or {}

        def json(self):
            return self._json

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.RequestException("HTTP error")

    return FakeResponse()

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_fetch_transactions(mock_get):
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
    mock_get.return_value = fake_response()
    mock_put.return_value = fake_response()

    client = FireflyClient(BASE_URL, HEADERS)
    client.update_transaction_description("123", "new desc")

    mock_put.assert_called_once()
    args, kwargs = mock_put.call_args
    assert "new desc" in str(kwargs["json"])

@patch("fireflyiii_enricher_core.firefly_client.requests.post")
def test_add_tag_to_transaction(mock_post):
    mock_post.return_value = fake_response()

    client = FireflyClient(BASE_URL, HEADERS)
    client.add_tag_to_transaction("123", tag_id=999)

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"] == {"tags": ["999"]}

@patch("fireflyiii_enricher_core.firefly_client.requests.put")
@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_update_transaction_notes(mock_get, mock_put):
    mock_get.return_value = fake_response(json_data={"data": {"id": "123", "attributes": {"description": "desc"}}})
    mock_put.return_value = fake_response()

    client = FireflyClient(BASE_URL, HEADERS)
    client.update_transaction_notes("123", new_notes="note test")

    mock_put.assert_called_once()
    args, kwargs = mock_put.call_args
    assert kwargs["json"]["transactions"][0]["notes"] == "note test"

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_fetch_transactions_http_error(mock_get):
    mock_get.return_value = fake_response(status_code=500)
    client = FireflyClient(BASE_URL, HEADERS)
    with pytest.raises(Exception):
        client.fetch_transactions()

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
def test_update_transaction_description_http_error_on_get(mock_get):
    mock_get.return_value = fake_response(status_code=404)
    client = FireflyClient(BASE_URL, HEADERS)
    client.update_transaction_description("123", "test")  # Should not raise, but log error

@patch("fireflyiii_enricher_core.firefly_client.requests.get")
@patch("fireflyiii_enricher_core.firefly_client.requests.put")
def test_update_transaction_description_http_error_on_put(mock_put, mock_get):
    mock_get.return_value = fake_response()
    mock_put.return_value = fake_response(status_code=500)
    client = FireflyClient(BASE_URL, HEADERS)
    client.update_transaction_description("123", "test")  # Should not raise, but log error
