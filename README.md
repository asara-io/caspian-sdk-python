# Caspian SDK for Python

The Caspian SDK for Python is the official Python client library for the public
Caspian API. Caspian provides policy-aware access to market data and related
metadata through authenticated HTTPS endpoints.

This repository contains the Python distribution that will be published as
`asara-caspian`, with import path `asara.caspian`.

## Status

This SDK is in early development. The synchronous client currently supports the
authenticated public health endpoint.

## Installation

Once released through PyPI:

```sh
python -m pip install asara-caspian
```

For local development from this repository:

```sh
python -m pip install -e ".[dev]"
python -m pytest
```

## Authentication

Caspian public API requests authenticate with an API key. The SDK will support
the same credentials accepted by the service:

- `Authorization: Bearer <api-key>`
- `X-API-Key: <api-key>`

Applications should load API keys from environment variables, secret stores, or
deployment-specific credential managers. Do not commit API keys to source
control.

## Example

The completed SDK is expected to expose typed sync and async clients for the
external Caspian API. The synchronous health check is available now:

```python
import os

from asara.caspian import CaspianClient


with CaspianClient(
    base_url="https://api.caspian.example.com",
    api_key=os.environ["CASPIAN_API_KEY"],
) as client:
    health = client.health()

print(health)
```

Market data and policy resources will follow the same client layout as they are
added. Async usage is expected to follow the same resource layout:

```python
import os

from asara.caspian import AsyncCaspianClient


async with AsyncCaspianClient(
    base_url="https://api.caspian.example.com",
    api_key=os.environ["CASPIAN_API_KEY"],
) as client:
    samples = await client.market_data.enriched_samples(ticker="AAPL", limit=100)
```

The final API may evolve while the package remains pre-1.0.

## Public API Coverage

The public SDK will focus on customer-facing Caspian APIs:

- Service health checks.
- Policy-filtered market data samples.
- Policy-filtered enriched market data samples.
- Active policy metadata visible to the authenticated customer.

Internal administrative, compliance, and gateway-only APIs are intentionally out
of scope for this public package.

## Package Layout

The Python distribution name is `asara-caspian`. The import path is
`asara.caspian`.

Expected module areas:

- `asara.caspian.CaspianClient` for synchronous API access.
- `asara.caspian.AsyncCaspianClient` for asynchronous API access.
- `asara.caspian.market_data` for market sample reads.
- `asara.caspian.policy` for customer-visible policy metadata.
- `asara.caspian.errors` for typed SDK and service errors.

## Development

## Build and Test

Create and activate a virtual environment using your platform's usual workflow,
then install the SDK in editable mode with development dependencies:

```sh
python -m pip install -e ".[dev]"
```

Run the test suite:

```sh
python -m ruff check src tests
python -m mypy src
python -m pytest
```

Build source and wheel distributions:

```sh
python -m pip install build
python -m build
```

## License

Copyright 2026 Asara LLC.

Licensed under the Apache License, Version 2.0. See `LICENSE`.
