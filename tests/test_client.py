import pytest
import requests
from unittest.mock import patch
from fireflyiii_enricher_core.firefly_client import FireflyClient


BASE_URL = "https://demo.firefly.local"
TOKEN = "test-token"


def fake_response(status_code=200, json_data=None):
    class FakeResponse:
        def __init__(self):
            self.status_code = status_code
            self._json = json_data or {}

        def json(self):
            return self._json

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError("HTTP error")

    return FakeResponse()


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_fetch_transactions(mock_request):
    mock_request.return_value = fake_response(json_data={
        "data": [{"id": "123", "attributes": {"transactions": [{"description": "test"}]}}],
        "links": {"next": None}
    })

    client = FireflyClient(BASE_URL, TOKEN)
    result = client.fetch_transactions()
    assert len(result) == 1
    assert result[0]["id"] == "123"


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_update_description_success(mock_request):
    mock_request.side_effect = [
        fake_response(json_data={
            "data": {
                "id": "123",
                "attributes": {
                    "transactions": [{"description": "old"}]
                }
            }
        }),
        fake_response()
    ]
    client = FireflyClient(BASE_URL, TOKEN)
    client.update_transaction_description("123", "new")
    assert mock_request.call_count == 2


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_update_transaction_notes_success(mock_request):
    mock_request.side_effect = [
        fake_response(json_data={
            "data": {
                "id": "123",
                "attributes": {
                    "transactions": [{"notes": "old"}]
                }
            }
        }),
        fake_response()
    ]
    client = FireflyClient(BASE_URL, TOKEN)
    client.update_transaction_notes("123", "new note")
    assert mock_request.call_count == 2


@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_add_tag_to_transaction(mock_request):
    mock_request.side_effect = [
        fake_response(json_data={
            "data": {
                "id": "123",
                "attributes": {
                    "transactions": [{"tags": ["existing"]}]
                }
            }
        }),
        fake_response()
    ]
    client = FireflyClient(BASE_URL, TOKEN)
    client.add_tag_to_transaction("123", "new-tag")
    assert mock_request.call_count == 2

@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_json_decode_error(mock_request):
    class BadJsonResponse:
        def raise_for_status(self): pass
        def json(self): raise ValueError("bad json")

    mock_request.return_value = BadJsonResponse()
    client = FireflyClient(BASE_URL, TOKEN)
    with pytest.raises(RuntimeError, match="Failed to parse JSON response"):
        client.fetch_transactions()



@patch("fireflyiii_enricher_core.firefly_client.requests.request")
def test_timeout_handling(mock_request):
    mock_request.side_effect = requests.Timeout()
    client = FireflyClient(BASE_URL, TOKEN)
    with pytest.raises(RuntimeError, match="Request timed out"):
        client.fetch_transactions()
