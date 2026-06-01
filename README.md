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

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

**Gradio demo for [cloudfit-core](https://github.com/cloudfit-io/cloudfit-core).** Pick a workload, get a ranked list of GCP machine types scored on cost, performance, and availability.

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

`data/gcp_snapshot.json` is a representative sample of GCP Compute Engine across `us-central1`, `us-east1`, `us-west1`, `europe-west4`, and `asia-southeast1`. 875 entries total. Prices are adjusted with approximate per-region multipliers. Not live pricing: regenerate with [cloudfit-provider-gcp](https://github.com/cloudfit-io/cloudfit-provider-gcp) if you need fresher numbers.

## Ecosystem

- [`cloudfit-core`](https://github.com/cloudfit-io/cloudfit-core): scoring engine
- [`cloudfit-api`](https://github.com/cloudfit-io/cloudfit-api): HTTP API
- [`cloudfit-provider-gcp`](https://github.com/cloudfit-io/cloudfit-provider-gcp): GCP machine-type fetcher
- [`cloudfit-provider-aws`](https://github.com/cloudfit-io/cloudfit-provider-aws): AWS provider (planning phase)

## License

Apache 2.0: see [LICENSE](LICENSE).
