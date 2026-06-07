# Copyright 2026 Asara LLC
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from types import TracebackType
from typing import Literal, cast

import httpx

from asara.caspian.errors import (
    CaspianAPIError,
    CaspianDecodeError,
    CaspianTransportError,
)
from asara.caspian.models import HealthResponse

AuthHeader = Literal["authorization", "x-api-key"]


class CaspianClient:
    """Synchronous client for the public Caspian API."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float | httpx.Timeout = 10.0,
        auth_header: AuthHeader = "authorization",
        http_client: httpx.Client | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._auth_header = auth_header
        self._client = http_client or httpx.Client(timeout=timeout)
        self._owns_client = http_client is None

    def __enter__(self) -> CaspianClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def health(self) -> HealthResponse:
        """Return the service health status for the authenticated API key."""

        response = self._request("GET", "/api/v1/health")
        try:
            payload = response.json()
        except ValueError as exc:
            raise CaspianDecodeError(
                "Caspian health response was not valid JSON.",
                status_code=response.status_code,
                request_id=_request_id(response),
            ) from exc

        if not isinstance(payload, dict):
            raise CaspianDecodeError(
                "Caspian health response must be a JSON object.",
                status_code=response.status_code,
                request_id=_request_id(response),
            )

        return HealthResponse.from_json(payload)

    def _request(self, method: str, path: str) -> httpx.Response:
        url = f"{self._base_url}{path}"
        try:
            response = self._client.request(method, url, headers=self._auth_headers())
        except httpx.TransportError as exc:
            raise CaspianTransportError(str(exc)) from exc

        if response.status_code >= 400:
            raise CaspianAPIError(
                "Caspian API request failed.",
                status_code=response.status_code,
                request_id=_request_id(response),
                response_text=response.text,
            )

        return response

    def _auth_headers(self) -> dict[str, str]:
        if self._auth_header == "authorization":
            return {"Authorization": f"Bearer {self._api_key}"}
        if self._auth_header == "x-api-key":
            return {"X-API-Key": self._api_key}

        raise ValueError(f"Unsupported auth header: {self._auth_header}")


def _request_id(response: httpx.Response) -> str | None:
    request_id = cast(str | None, response.headers.get("X-Request-ID"))
    if request_id is not None:
        return request_id
    return cast(str | None, response.headers.get("X-Caspian-Request-ID"))
