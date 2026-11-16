from dataclasses import dataclass, field
import math
import os
from urllib.parse import urlparse


@dataclass(frozen=True)
class Settings:
    base_url: str = "https://reqres.in/api"
    api_key: str = field(default="", repr=False)
    timeout: float = 10

    def __post_init__(self):
        parsed = urlparse(self.base_url)
        if (parsed.scheme not in {"http", "https"} or not parsed.netloc
                or parsed.username or parsed.password or parsed.query or parsed.fragment):
            raise ValueError("Base URL must be an HTTP(S) origin/path without credentials, query or fragment")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("Timeout must be a finite positive number")

    @classmethod
    def from_env(cls):
        return cls(base_url=os.getenv("REQRES_BASE_URL", cls.base_url),
                   api_key=os.getenv("REQRES_API_KEY", ""),
                   timeout=float(os.getenv("REQUEST_TIMEOUT", "10")))
