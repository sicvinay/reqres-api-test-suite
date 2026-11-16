import json
from pathlib import Path
import pytest
from utils.data_loader import load_test_data
from utils.contracts import response_json

RESPONSES = Path(__file__).resolve().parents[1] / "data" / "responses"


def fixture_response(name):
    with (RESPONSES / name).open(encoding="utf-8") as stream:
        return json.load(stream)


@pytest.mark.regression
@pytest.mark.smoke
def test_create_user_contract(users, client, requests_mock):
    payload = load_test_data("create_user.json")
    requests_mock.post(client.settings.base_url + "/users", status_code=201,
                       json=fixture_response("create_user.json"))
    response = users.create(payload)
    assert response.status_code == 201
    document = response_json(response, "created_user")
    assert {key: document[key] for key in payload} == payload
    assert requests_mock.last_request.json() == payload
    assert requests_mock.last_request.headers["Content-Type"] == "application/json"
    assert requests_mock.last_request.headers["x-api-key"] == "offline-test-key"


@pytest.mark.regression
@pytest.mark.smoke
def test_read_user_contract(users, client, requests_mock):
    identifier = load_test_data("read_user.json")["user_id"]
    requests_mock.get(client.settings.base_url + f"/users/{identifier}",
                      json=fixture_response("read_user.json"))
    response = users.read(identifier)
    assert response.status_code == 200
    assert response_json(response, "read_user")["data"]["id"] == identifier


@pytest.mark.regression
@pytest.mark.smoke
def test_update_user_contract(users, client, requests_mock):
    payload = load_test_data("update_user.json")
    requests_mock.put(client.settings.base_url + "/users/2",
                      json=fixture_response("update_user.json"))
    response = users.update(2, payload)
    assert response.status_code == 200
    document = response_json(response, "updated_user")
    assert {key: document[key] for key in payload} == payload
    assert requests_mock.last_request.json() == payload


@pytest.mark.regression
@pytest.mark.smoke
def test_delete_user_has_empty_body(users, client, requests_mock):
    identifier = load_test_data("delete_user.json")["id"]
    requests_mock.delete(client.settings.base_url + f"/users/{identifier}", status_code=204)
    response = users.delete(identifier)
    assert response.status_code == 204
    assert response.content == b""
    assert requests_mock.last_request.method == "DELETE"
