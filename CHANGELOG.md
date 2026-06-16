# Changelog

## [1.3.1] - 2026-06-16

### Added

- Added a controlled tag vocabulary with method, domain, resource, and person groups.
- Added tag normalization helpers and a local tag audit script for Codex curation.
- Added README wording for Codex-agent-assisted automation.

### Changed

- Normalized existing tags and conservatively added clear tags to selected rows.
- Updated README generation to canonicalize, deduplicate, and link configured tags.
- Updated `awe-check` to warn on unknown or alias tags without failing validation.
- Switched the GitHub stars badge to `badgen.net` because Shields currently returns a GitHub token-pool error for this repo.
- Set package version to `1.3.1`.

## [1.3.0] - 2026-06-16

### Added

- Added a full paper-read scan pass with curated peptide and peptide-computation entries.
- Added arXiv metadata fallback for paper-read rows whose DOI is not indexed by Crossref.

### Changed

- Reworked the section and subsection taxonomy around paper-reading tasks and user workflows.
- Reclassified existing curated rows and paper-read rows into the new taxonomy.
- Updated selected preprint entries to their final journal DOI metadata.
- Set package version to `1.3.0`.

## [1.2.0] - 2026-06-16

### Added

- Added `data/paper-read.csv` as a minimal paper-read source table.
- Added live Crossref enrichment for paper-read rows during README generation.
- Added optional Crossref enrichment to the paper-read candidate scanner.

### Changed

- Updated `awe-check` to validate both curated and paper-read paper sources.
- Set package version to `1.2.0`.

## [1.1.0] - 2026-06-16

### Added

- Added `paper-read` as a local submodule at `vendor/paper-read`.
- Added a paper-read candidate scanning workflow to the peptide curation skill.
- Added automation for ranking peptide-related notes before Codex curates entries into `data/paper.csv`.

### Changed

- Updated project guidance and CI to initialize submodules.
- Set package version to `1.1.0`.

## [1.0.0] - 2026-06-16

### Added

- Added repo-local Codex skills for paper curation and tooling maintenance.
- Added `AGENTS.md` with project-level agent workflow guidance.
- Added minimal GitHub Actions CI for validation and packaging.

### Changed

- Migrated packaging metadata from `setup.py` to `pyproject.toml`.
- Updated contributor documentation for current commands and project layout.
- Set package version to `1.0.0`.

### Fixed

- Aligned package license metadata with the GPLv3 `LICENSE` file.
- Made `awe-check` suitable for CI failure detection.
