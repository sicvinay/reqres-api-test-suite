import pytest
import requests
from jsonschema import ValidationError
from utils.contracts import response_json
from utils.data_loader import load_test_data

pytestmark = [pytest.mark.negative, pytest.mark.regression]


@pytest.mark.parametrize("method", ["create", "update"])
@pytest.mark.parametrize("payload", [{"job": "QA"}, {"name": "", "job": "QA"},
                                     {"name": "Demo", "job": None}])
def test_invalid_payload_is_rejected_before_http(users, requests_mock, method, payload):
    with pytest.raises(ValidationError):
        if method == "create":
            users.create(payload)
        else:
            users.update(2, payload)
    assert requests_mock.call_count == 0


@pytest.mark.parametrize("operation", ["read", "update", "delete"])
@pytest.mark.parametrize("identifier", ["abc", 0, -1, True])
def test_invalid_id_is_rejected_before_http(users, requests_mock, operation, identifier):
    with pytest.raises(ValueError, match="positive integer"):
        if operation == "update":
            users.update(identifier, {"name": "Demo", "job": "QA"})
        else:
            getattr(users, operation)(identifier)
    assert requests_mock.call_count == 0


def test_missing_user_response_is_preserved(users, client, requests_mock):
    requests_mock.get(client.settings.base_url + "/users/23", status_code=404, json={})
    response = users.read(23)
    assert response.status_code == 404
    assert response.json() == {}


def test_malformed_api_json_raises_clear_error(users, client, requests_mock):
    requests_mock.get(client.settings.base_url + "/users/2", text="{broken")
    with pytest.raises(ValueError, match="not valid JSON"):
        response_json(users.read(2), "read_user")


@pytest.mark.parametrize("body", [{}, {"data": {"id": "wrong-type"}}, {"data": {"id": 2}}])
def test_broken_read_contract_is_detected(users, client, requests_mock, body):
    requests_mock.get(client.settings.base_url + "/users/2", json=body)
    with pytest.raises(ValidationError):
        response_json(users.read(2), "read_user")


@pytest.mark.parametrize("failure", [requests.exceptions.Timeout, requests.exceptions.ConnectionError])
def test_transport_failure_propagates(users, client, requests_mock, failure):
    requests_mock.get(client.settings.base_url + "/users/2", exc=failure("simulated failure"))
    with pytest.raises(failure):
        users.read(2)


def test_invalid_input_json_file_is_rejected(tmp_path):
    (tmp_path / "broken.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_test_data("broken.json", directory=tmp_path)
