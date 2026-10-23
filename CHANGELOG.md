# Changelog

All notable changes to `cloudfit-ui` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_No unreleased changes._

## [0.2.2] - 2026-10-23

### Changed
- Require `cloudfit-core>=0.8.2`.

## [0.2.1] - 2026-10-23

### Added
- Smoke tests (`tests/test_app.py`) and a CI workflow running ruff, `mypy --strict`, and pytest on every pull request and push to main.

### Changed
- "About the snapshot" now says prices are refreshed weekly from the GCP billing catalog and shows the last refresh date (kept current by cloudfit-provider-gcp's refresh workflow); GPU prices are noted as approximate.

## [0.2.0] - 2026-10-22

### Added
- Scoring-depth surfacing (requires cloudfit-core 0.8.0): a "Pricing mode" dropdown (`auto` / `on_demand` / `spot` / `cud_1yr`, where `auto` lets the archetype pick), a "why" column and a "Why" line in the summary showing each pick's `reason`. The bundled snapshot is enriched with `perf_factor` (all instances), `gpu_type` (all GPU instances), and real `spot_price_hr` / `cud_1yr_price_hr` plus refreshed on-demand prices from a live `cloudfit-provider-gcp` fetch (CPU/RAM instances; GPU instances keep their full on-demand price and have no spot/CUD). The demo scores effective capacity, GPU throughput, and spot/committed-use pricing.
- Headroom controls (requires cloudfit-core 0.5.0): a "Headroom" dropdown offering multiplier presets (1.0x to 2.0x) and a "Headroom mode" selector (hard / soft). The multiplier is converted to the fraction the engine expects (1.25x -> 0.25). Clicking an example resets headroom to none so the form and result stay in sync.

### Changed
- Require `cloudfit-core>=0.8.0`.

### Fixed
- `app.py` now passes `mypy --strict` (return-type annotations, `HeadroomMode` coercion); added `pyproject.toml` with a gradio-scoped mypy override.
- Displayed price/hr and $/mo now use the pricing mode the ranking was scored with (spot or committed-use when the instance has that price, else on-demand), instead of always showing on-demand. The cost explainer notes cost is per unit of work, and `SNAPSHOT_DATE` matches the refreshed snapshot.
- Corrected perf/cost explanation text for cloudfit-core 0.4.0; archetype hint now notes it does not affect ranking.

## [0.1.0] - 2026-05-31

### Added
- Initial Gradio demo UI over `cloudfit-core` 0.3.0 (fit-based scoring).
- Workload profile form: vCPU, RAM, archetype, optimize-for, multi-region, GPU.
- Five built-in example workloads (BWA-MEM2, Cell Ranger, AlphaFold, Nextflow burst, Spark ETL).
- Ranked output: top pick summary + DataFrame of the top-N candidates with hourly and monthly cost.
- Bundled GCP machine-type snapshot (875 entries across five regions).
- Hugging Face Space deployment metadata in README frontmatter.

[0.2.2]: https://github.com/cloudfit-io/cloudfit-ui/releases/tag/v0.2.2
[0.2.1]: https://github.com/cloudfit-io/cloudfit-ui/releases/tag/v0.2.1
[0.2.0]: https://github.com/cloudfit-io/cloudfit-ui/releases/tag/v0.2.0
[0.1.0]: https://github.com/cloudfit-io/cloudfit-ui/releases/tag/v0.1.0
