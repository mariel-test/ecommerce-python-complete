import requests
from urllib.parse import unquote_plus
from typing import Optional, Any, Dict
from enum import Enum


class ContentType(str, Enum):
    """Content type enum for API requests."""

    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"


def _log_response(response: requests.Response, *args: Any, **kwargs: Any) -> None:
    req = response.request
    method = req.method
    url = response.url

    body_str = ""
    if req.body:
        raw = req.body if isinstance(req.body, str) else req.body.decode("utf-8", errors="replace")
        body_str = unquote_plus(raw)

    try:
        rj = response.json()
        code = rj.get("responseCode", "")
        msg = rj.get("message", "")
        result = f"responseCode={code}" + (f'  "{msg}"' if msg else "")
    except Exception:
        result = response.text[:200]

    sep = "─" * 64
    print(f"\n{sep}")
    print(f"  {method:<7} {url}")
    if body_str:
        print(f"  payload  {body_str}")
    print(f"  ← {response.status_code}    {result}")
    print(sep)


class ApiClient:
    """HTTP client for API requests using requests library."""

    def __init__(self, base_url: str) -> None:
        """Initialize API client with base URL."""
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.hooks["response"].append(_log_response)

    def _url(self, path: str) -> str:
        """Build full URL from base URL and path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> requests.Response:
        """Perform GET request."""
        return self.session.get(self._url(path), params=params, **kwargs)

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Perform POST request."""
        return self.session.post(self._url(path), json=json, data=data, **kwargs)

    def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Perform PUT request."""
        return self.session.put(self._url(path), json=json, data=data, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        """Perform DELETE request."""
        return self.session.delete(self._url(path), **kwargs)
