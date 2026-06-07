# Copyright 2026 Asara LLC
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from asara.caspian.errors import CaspianDecodeError


@dataclass(frozen=True, slots=True)
class HealthResponse:
    """Health status returned by the public Caspian API."""

    service: str
    status: str
    version: str

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> HealthResponse:
        service = _required_string(payload, "service")
        status = _required_string(payload, "status")
        version = _required_string(payload, "version")
        return cls(service=service, status=status, version=version)


def _required_string(payload: dict[str, Any], field_name: str) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str):
        raise CaspianDecodeError(
            f"Caspian response field {field_name!r} must be a string.",
        )
    return value
