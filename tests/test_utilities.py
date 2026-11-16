import logging
import pytest
from utils.config import Settings
from utils.data_loader import load_test_data


@pytest.mark.parametrize("url", ["relative", "ftp://example.test", "https://user:secret@example.test"])
def test_invalid_base_url(url):
    with pytest.raises(ValueError):
        Settings(base_url=url)


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_invalid_timeout(timeout):
    with pytest.raises(ValueError):
        Settings(timeout=timeout)


def test_environment_configuration(monkeypatch):
    monkeypatch.setenv("REQRES_API_KEY", "private-test-value")
    monkeypatch.setenv("REQUEST_TIMEOUT", "3.5")
    settings = Settings.from_env()
    assert settings.timeout == 3.5
    assert settings.api_key == "private-test-value"
    assert "private-test-value" not in repr(settings)


def test_data_load_is_independent_of_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert load_test_data("create_user.json")["job"] == "QA Engineer"


def test_missing_payload_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_test_data("missing.json", directory=tmp_path)


def test_data_path_traversal_is_rejected():
    with pytest.raises(ValueError):
        load_test_data("../requirements.txt")


def test_timeout_is_passed_to_transport(client, monkeypatch):
    captured = {}

    def request(method, url, **kwargs):
        captured.update(kwargs)
        raise TimeoutError("stop before HTTP")

    monkeypatch.setattr(client.session, "request", request)
    with pytest.raises(TimeoutError):
        client.request("GET", "/users/2")
    assert captured["timeout"] == client.settings.timeout


def test_logging_does_not_leak_key_or_payload(users, client, requests_mock, caplog):
    requests_mock.get(client.settings.base_url + "/users/2", json={"private": "response-secret"})
    with caplog.at_level(logging.INFO):
        users.read(2)
    assert "HTTP 200" in caplog.text
    assert "offline-test-key" not in caplog.text
    assert "response-secret" not in caplog.text
