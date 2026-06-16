# Repo Content Map

Use this reference to orient content work in `awesome-peptide`.

## Main Files

- `data/paper.csv`: canonical table of manually curated papers.
- `data/paper-read.csv`: minimal table for paper-read sourced entries enriched from Crossref or arXiv during README generation.
- `awepep/crossref.py`: Crossref Work API and arXiv API helpers for live paper-read metadata enrichment.
- `awepep/config.py`: section/subsection ordering, controlled tag groups, tag aliases, tag links, `max_pined`, and `last_days`.
- `awepep/tags.py`: shared tag splitting, canonicalization, warning, and README-link formatting helpers.
- `awepep/template.py`: Liquid templates for header, paper rows, table of contents, pinned papers, recent papers, and footer.
- `awepep/paper.py`: loads CSV, formats tags, sorts papers, merges `DATABASE.md`, and writes `README.md`.
- `awepep/check.py`: validates required fields, sections, DOI extraction, duplicate DOI values, pinned count, tag warnings, and prints statistics.
- `DATABASE.md`: manually maintained Chapter 0 content inserted into generated README.
- `README.md`: generated public list; do not edit generated paper sections directly.
- `CONTRIBUTING.md`: setup and contribution instructions.
- `pyproject.toml`: dependencies and console entrypoints.
- `vendor/paper-read`: git submodule containing upstream paper-reading notes used for candidate discovery.

## Generation Flow

`PaperList("data/paper.csv").get_md(write=True)`:

1. Reads `data/paper.csv`.
2. Reads `data/paper-read.csv` if present.
3. Fetches Crossref or arXiv metadata for paper-read DOIs and converts rows into the main render shape.
4. Deduplicates paper-read rows against `data/paper.csv` by DOI.
5. Adds bold year formatting to `publish_date_`.
6. Canonicalizes, deduplicates, and converts configured tags to Markdown links.
7. Sorts papers by `publish_date` descending.
8. Builds recent papers using `last_days = 180`.
9. Builds pinned papers from rows where `pined` is truthy.
10. Renders the cover image, generated table of contents, `DATABASE.md`, paper sections, footer, and citations.
11. Writes `README.md`.

## Current Project Facts

- `data/paper.csv` currently has 51 paper rows.
- `data/paper-read.csv` currently has 28 paper-read source rows.
- Both CSV files currently have no duplicate DOI values under the checker regex.
- `quality` is currently either blank or `high`.
- `pined` is currently blank or `true`; Pandas displays these as false/true booleans after loading.
- `README.md` contains a top update-frequency note that is present in `awepep/template.py`.
- README generation uses the Crossref API and arXiv fallback when `data/paper-read.csv` contains rows.
- Tag validation uses controlled vocabulary warnings instead of hard failures for unknown tags.
- Console commands are defined in `pyproject.toml` as `awe-pep` and `awe-check`.
- `vendor/paper-read` is a source-only submodule; update it, scan it, but do not edit files inside it.

## Command Notes

Install dependencies before running the generator or checker:

```bash
pip install -e .
```

Console commands from `pyproject.toml`:

```bash
awe-pep
awe-check
```

Fallback module commands:

```bash
python -m awepep.main
python -m awepep.check
```

Paper-read source commands:

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
python .codex/skills/curate-peptide-papers/scripts/scan_paper_read_candidates.py --limit 200 --enrich-crossref
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py
```
