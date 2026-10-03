---
name: curate-peptide-papers
description: Discover, verify and curate peptide research across design, synthesis, biology, delivery, materials and applications. Use for paper-read submodule scans, Crossref/PubMed/arXiv discovery, paper CSV classification and tags, metadata snapshots, deduplication and generated README updates.
---

# Curate Peptide Papers

Use `data/paper.csv` for manual entries and `data/paper-read.csv` for minimal note-sourced rows. README is generated, and the vendor submodule is read-only.

## Choose The Workflow

- For discovery and classification, read [paper-curation.md](references/paper-curation.md).
- For note scans and source rows, read [paper-read-source.md](references/paper-read-source.md).
- For file ownership and generation, read [repo-content-map.md](references/repo-content-map.md).

Inspect `git status --short` and the current `awepep.config.sections`/`tag_groups` before editing. Do not infer permission to commit, push, merge or schedule from a paper-discovery request.

## Discover On Demand

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
awe-discover --since 2026-06-16 --until 2026-10-03 --limit 200
```

Replace the example window with the requested dates. Reports include provider coverage, errors, truncation and candidate status. Inspect the report even when the command fails. Do not retry without bounds or claim completeness from a capped search. No scheduled Actions are needed.

## Curate

1. Review candidate title, abstract and primary source for substantive peptide relevance. AI is not required.
2. Verify DOI and publication date; never use note month or API registration date as publication evidence.
3. Deduplicate across both CSVs by normalized DOI, related preprint/journal identifiers and normalized title.
4. Choose one primary contribution-based section/subsection from config. Use canonical tags for secondary topics.
5. Add accepted rows only after editorial review; do not blindly append scanner output. Leave uncertain links, quality and pinned fields blank.
6. Refresh metadata snapshots for paper-read changes, then validate and regenerate offline with a fixed reference date.
7. Report additions, migrations, skipped cases and coverage limits separately.

## Validate And Render

```bash
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py --strict
python -m unittest discover -s tests -v
awe-pep --refresh-metadata --as-of 2026-10-03
awe-pep --offline --as-of 2026-10-03
git diff -- data README.md
```

Use `PaperList("data/paper.csv", offline=True).get_md(write=False, as_of="2026-10-03")` for read-only verification. Never hand-edit generated paper sections or files inside `vendor/paper-read`.
