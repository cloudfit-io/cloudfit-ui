# Changelog

All notable changes to `cloudfit-ui` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-06-02

### Added
- Headroom controls (requires cloudfit-core 0.5.0): a "Headroom" dropdown offering multiplier presets (1.0x to 2.0x) and a "Headroom mode" selector (hard / soft). The multiplier is converted to the fraction the engine expects (1.25x -> 0.25). Clicking an example resets headroom to none so the form and result stay in sync.

### Changed
- Require `cloudfit-core>=0.5.0`.

### Fixed
- Corrected perf/cost explanation text for cloudfit-core 0.4.0; archetype hint now notes it does not affect ranking.

## [0.1.0] - 2026-05-31

### Added
- Initial Gradio demo UI over `cloudfit-core` 0.3.0 (fit-based scoring).
- Workload profile form: vCPU, RAM, archetype, optimize-for, multi-region, GPU.
- Five built-in example workloads (BWA-MEM2, Cell Ranger, AlphaFold, Nextflow burst, Spark ETL).
- Ranked output: top pick summary + DataFrame of the top-N candidates with hourly and monthly cost.
- Bundled GCP machine-type snapshot (875 entries across five regions).
- Hugging Face Space deployment metadata in README frontmatter.

[0.1.0]: https://github.com/cloudfit-io/cloudfit-ui/releases/tag/v0.1.0
