import requests
from typing import Any, Dict, Optional


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return requests.get(self._url(path), params=params, **kwargs)

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        return requests.post(self._url(path), json=json, data=data, **kwargs)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return requests.put(self._url(path), json=json, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return requests.delete(self._url(path), **kwargs)
