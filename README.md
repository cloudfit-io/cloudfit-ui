---
title: cloudfit
emoji: 🖥️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: apache-2.0
short_description: Pick a workload, get a cloud machine-type recommendation.
---

# cloudfit-ui

[![Release](https://img.shields.io/github/v/release/cloudfit-io/cloudfit-ui)](https://github.com/cloudfit-io/cloudfit-ui/releases)
[![CI](https://github.com/cloudfit-io/cloudfit-ui/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudfit-io/cloudfit-ui/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

**Gradio demo for [cloudfit-core](https://github.com/cloudfit-io/cloudfit-core).** Pick a workload and a pricing mode, get a ranked list of GCP machine types scored on cost, performance, and availability, with a one-line reason for each pick.

Live demo: **[chaitanyakasaraneni-cloudfit-ui.hf.space](https://chaitanyakasaraneni-cloudfit-ui.hf.space)**

---

## What this is

A one-screen UI that runs the cloudfit scoring engine in-process against a bundled GCP machine-type snapshot. No login, no credentials, no provider calls at request time. It exists so you can try cloudfit in 30 seconds before reading any code.

For programmatic access, use the [HTTP API](https://github.com/cloudfit-io/cloudfit-api) instead.

## Run locally

```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:7860
```

## About the snapshot

`data/gcp_snapshot.json` is a representative sample of GCP Compute Engine across `us-central1`, `us-east1`, `us-west1`, `europe-west4`, and `asia-southeast1`. 875 entries total, each with a `perf_factor`, and GPU instances with a `gpu_type`. On-demand, spot, and 1-year committed-use prices for CPU/RAM machine types are refreshed weekly from the live GCP billing catalog by [cloudfit-provider-gcp](https://github.com/cloudfit-io/cloudfit-provider-gcp)'s scheduled workflow, which opens a pull request here. GPU instances keep approximate on-demand prices and have no spot or committed-use price.

## Development

```bash
pip install -r requirements.txt pytest mypy "ruff>=0.15,<0.16"
pytest                 # smoke tests in tests/
ruff check app.py tests/ && mypy --strict app.py
```

CI runs the same checks on every pull request, against the Gradio version the Space runs (`sdk_version` in this README's front matter, currently 5.49.1). `requirements.txt` allows Gradio 5 or 6, so install `gradio==5.49.1` locally to match the live demo exactly.

## Ecosystem

- [`cloudfit-core`](https://github.com/cloudfit-io/cloudfit-core): scoring engine
- [`cloudfit-api`](https://github.com/cloudfit-io/cloudfit-api): HTTP API
- [`cloudfit-provider-gcp`](https://github.com/cloudfit-io/cloudfit-provider-gcp): GCP machine-type fetcher
- [`cloudfit-provider-aws`](https://github.com/cloudfit-io/cloudfit-provider-aws): AWS provider (planning phase)

## License

Apache 2.0: see [LICENSE](LICENSE).
