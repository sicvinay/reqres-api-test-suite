import pytest
from utils.config import Settings
from utils.request_helper import ApiClient
from utils.users import UsersApi


def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", help="Enable real ReqRes demo requests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--live"):
        for item in items:
            if "live" in item.keywords:
                item.add_marker(pytest.mark.skip(reason="Real API disabled; pass --live to opt in"))


@pytest.fixture
def client():
    # Offline tests use a reserved domain and cannot accidentally contact ReqRes.
    with ApiClient(Settings(base_url="https://reqres.example.test/api", api_key="offline-test-key")) as instance:
        yield instance


@pytest.fixture
def users(client):
    return UsersApi(client)


@pytest.fixture
def live_users():
    with ApiClient() as client:
        # Keep live mode limited to ReqRes's non-persistent demo surface.
        if client.settings.base_url.rstrip("/") != "https://reqres.in/api":
            raise pytest.UsageError("Live tests require https://reqres.in/api")
        yield UsersApi(client)
