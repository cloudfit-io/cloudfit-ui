# Changelog

All notable changes to `cloudfit-ui` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-31

### Added
- Initial Gradio demo UI over `cloudfit-core` 0.2.0.
- Workload profile form: vCPU, RAM, archetype, optimize-for, region, GPU.
- Five built-in example workloads (BWA-MEM2, Cell Ranger, AlphaFold, Nextflow burst, Spark ETL).
- Ranked output: top pick summary + DataFrame of the top-N candidates with hourly and monthly cost.
- Bundled GCP machine-type snapshot (875 entries across five regions).
- Hugging Face Space deployment metadata in README frontmatter.

[0.1.0]: https://github.com/cloudfit-io/cloudfit-ui/releases/tag/v0.1.0
