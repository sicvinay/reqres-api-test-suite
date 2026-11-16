"""Session-scoped transport. Never logs credentials, payloads or response bodies."""
import logging
import requests
from utils.config import Settings

log = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, settings=None):
        self.settings = settings or Settings.from_env()
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if self.settings.api_key:
            self.session.headers["x-api-key"] = self.settings.api_key

    def request(self, method, endpoint, *, payload=None, params=None):
        if not endpoint.startswith("/") or endpoint.startswith("//") or "://" in endpoint:
            raise ValueError("Use a relative endpoint starting with one slash")
        response = self.session.request(
            method, self.settings.base_url.rstrip("/") + endpoint,
            json=payload, params=params, timeout=self.settings.timeout,
        )
        # Log no URLs/queries or headers; they may contain secrets.
        log.info("%s -> HTTP %s in %.3fs", method, response.status_code,
                 response.elapsed.total_seconds())
        return response

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
