# Copyright 2026 Asara LLC
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import httpx
import pytest

from asara.caspian import CaspianAPIError, CaspianClient, HealthResponse


def test_health_sends_bearer_token_and_decodes_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == "https://api.example.test/api/v1/health"
        assert request.headers["Authorization"] == "Bearer cas_demo_key"
        return httpx.Response(
            200,
            json={
                "service": "caspian-customer-api",
                "status": "ok",
                "version": "0.1.0",
            },
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = CaspianClient(
        base_url="https://api.example.test",
        api_key="cas_demo_key",
        http_client=http_client,
    )

    assert client.health() == HealthResponse(
        service="caspian-customer-api",
        status="ok",
        version="0.1.0",
    )


def test_health_can_send_x_api_key_header() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert "Authorization" not in request.headers
        assert request.headers["X-API-Key"] == "cas_demo_key"
        return httpx.Response(
            200,
            json={
                "service": "caspian-customer-api",
                "status": "ok",
                "version": "0.1.0",
            },
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = CaspianClient(
        base_url="https://api.example.test/",
        api_key="cas_demo_key",
        auth_header="x-api-key",
        http_client=http_client,
    )

    assert client.health().status == "ok"


def test_health_raises_api_error_for_error_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401,
            headers={"X-Request-ID": "req_123"},
            json={"detail": "Unauthorized"},
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = CaspianClient(
        base_url="https://api.example.test",
        api_key="bad_key",
        http_client=http_client,
    )

    with pytest.raises(CaspianAPIError) as exc_info:
        client.health()

    assert exc_info.value.status_code == 401
    assert exc_info.value.request_id == "req_123"
    assert "Unauthorized" in (exc_info.value.response_text or "")
