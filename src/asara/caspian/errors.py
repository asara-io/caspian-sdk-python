# Copyright 2026 Asara LLC
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


class CaspianError(Exception):
    """Base exception for all Caspian SDK errors."""


class CaspianTransportError(CaspianError):
    """Raised when the SDK cannot reach the Caspian service."""


class CaspianAPIError(CaspianError):
    """Raised when the Caspian service returns an HTTP error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        request_id: str | None = None,
        response_text: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        self.response_text = response_text


class CaspianDecodeError(CaspianError):
    """Raised when the SDK cannot decode a Caspian service response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
