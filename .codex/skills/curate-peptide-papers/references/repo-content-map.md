# Repo Content Map

- `data/paper.csv`: canonical full entries, including DOI-less formal paper-read publications with a note link.
- `data/paper-read.csv`: minimal note-sourced formal DOI entries.
- `data/paper-archive.csv`: complete historical preprint records with archive date/reason, excluded from active generation/statistics.
- `data/paper-read-metadata.json`: versioned bibliographic snapshot with source and retrieval time.
- `awepep/discovery.py`: paper-read-first, non-mutating discovery and reports; external sources are opt-in.
- `awepep/publications.py`: shared DOI/official URL identities and preprint checks.
- `awepep/crossref.py`: paced/retried Crossref and arXiv metadata requests.
- `awepep/metadata.py`: cache-first, refresh and offline metadata modes.
- `awepep/config.py` / `tags.py`: ordered taxonomy and controlled tags.
- `awepep/paper.py` / `template.py`: CSV-to-README rendering.
- `awepep/check.py`: active/archive schema, classification, DOI/URL, date, flag and pinned-limit checks.
- `assets/`: cover image and linked reference PDFs.
- `DATABASE.md`: Chapter 0 resource tables; paper records belong in CSV.
- `vendor/paper-read`: external read-only source.
- `CONTRIBUTING.md`: maintained CLI, schema and validation guide.

## Rendering

PaperList reads both CSVs, obtains paper-read metadata from snapshots (or network when allowed), deduplicates identifiers, formats canonical tags and dates, orders sections/subsections by config and papers by publication date, and combines templates with DATABASE.md.

`get_md(write=False)` does not write README. `as_of` fixes the recent-paper reference date; `offline=True` prevents metadata requests. Only explicit refresh saves the snapshot. Missing records fail in offline mode. New snapshot records include source/retrieval time; primary-source date corrections retain `verified_publish_date`.

Commands after `python -m pip install -e ".[dev]"`:
`awe-discover`, `awe-check`, `awe-pep`.
Module fallbacks: `python -m awepep.discovery`, `python -m awepep.check`, `python -m awepep.main`.

Do not hardcode paper counts here; use the checker for current statistics.
