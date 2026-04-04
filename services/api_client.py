import logging
import requests
from requests import Response
from typing import Optional, Any, Dict
from enum import Enum


class ContentType(str, Enum):
    """Content type enum for API requests."""

    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"


class ApiClient:
    """HTTP client for API requests using requests library."""

    def __init__(self, base_url: str) -> None:
        """Initialize API client with base URL."""
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

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
        self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> requests.Response:
        """Perform PUT request."""
        return self.session.put(self._url(path), json=json, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        """Perform DELETE request."""
        return self.session.delete(self._url(path), **kwargs)
