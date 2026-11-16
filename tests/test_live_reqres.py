"""Real demo API coverage. Disabled unless --live is explicitly supplied."""
import pytest
from utils.contracts import response_json
from utils.data_loader import load_test_data

pytestmark = pytest.mark.live


def test_live_read_user(live_users):
    response = live_users.read(2)
    assert response.status_code == 200
    assert response_json(response, "read_user")["data"]["id"] == 2


def test_live_user_not_found(live_users):
    response = live_users.read(23)
    assert response.status_code == 404
    assert response.json() == {}


def test_live_create_user(live_users):
    payload = load_test_data("create_user.json")
    response = live_users.create(payload)
    assert response.status_code == 201
    document = response_json(response, "created_user")
    assert document["name"] == payload["name"]
    assert document["job"] == payload["job"]


def test_live_update_user(live_users):
    payload = load_test_data("update_user.json")
    response = live_users.update(2, payload)
    assert response.status_code == 200
    document = response_json(response, "updated_user")
    assert document["name"] == payload["name"]
    assert document["job"] == payload["job"]


def test_live_delete_user(live_users):
    response = live_users.delete(2)
    assert response.status_code == 204
    assert response.content == b""
