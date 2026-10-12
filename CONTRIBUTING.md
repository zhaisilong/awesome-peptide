# Contributing

Awesome Peptide covers peptide design, synthesis, biology, delivery, materials and applications, with both computational and experimental work.

## Setup

Python 3.9 or newer is required.

```bash
git clone --recurse-submodules git@github.com:zhaisilong/awesome-peptide.git
cd awesome-peptide
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Sources Of Truth

- `data/paper.csv`: manually verified paper metadata.
- `data/paper-read.csv`: minimal source rows from the read-only `vendor/paper-read` submodule.
- `data/paper-read-metadata.json`: tracked bibliographic snapshots with retrieval time and source.
- `data/paper-archive.csv`: historical preprints with archive date/reason, excluded from active lists and statistics.
- `DATABASE.md`: Chapter 0 resource tables and guides, not a second paper list.
- `awepep/config.py`: ordered taxonomy and canonical tag vocabulary.
- `awepep/template.py`: public README wording and formatting.
- `README.md`: generated output, not a paper-editing source.
- `.codex/skills/`: shared on-demand curation and maintenance workflows.
- `assets/`: cover image and reference PDFs linked by the generated README.

Keep CSV column order unchanged:

```text
title,sec,subsec,authors,publications,code,dataset,quality,publish_date,abstract,blogs,pined,tags
doi,title,source,sec,subsec,code,dataset,quality,pined,tags
```

Use a Markdown formal DOI link for `publications`, or an official stable HTTPS publication URL when no DOI exists. Verify venue/report status, authors/institution and publication date against primary evidence; a valid URL alone is not proof. Paper-read rows store a raw formal DOI and note path/permalink in `source`; do not duplicate bibliographic fields there. DOI-less paper-read publications use the full table with `[paper-read](NOTE_URL)` in `blogs`.

Archive columns are the full table columns followed by `archived_at,archive_reason`. Preserve original publication/source links and raw tags. First check for a formal version: update verified versions in the active table; otherwise archive, not delete. Later formal publication can restore a paper to the active list while retaining its archive history.

## On-Demand Discovery

Update the submodule only when discovering new notes:

```bash
git submodule update --init --recursive
git -C vendor/paper-read rev-parse HEAD
git submodule update --remote vendor/paper-read
git -C vendor/paper-read rev-parse HEAD
awe-discover --limit 200
```

Paper-read is the primary, owner-curated source. Compare the old/new commits and review new/changed notes first, then historical omissions. All substantive peptide research is in scope, not only AI. There is no publication-window cutoff for note-sourced work: place older publications chronologically. For changed accepted/archived notes, use the skill scanner with `--include-duplicates` and inspect the changed paths.

Independent discovery is an AIDD-focused supplement: target 2-3 accepted papers and never exceed 3 per run across all providers. Do not fill a quota with weak work; exceptional purely experimental work requires a stated significance rationale. Paper-read additions, version upgrades and metadata verification do not count toward this limit. External APIs are explicit opt-in:

```bash
awe-discover --sources crossref,pubmed --since YYYY-MM-DD --until YYYY-MM-DD --limit 10
```

Replace the dates with the requested window. Discovery writes Markdown/JSON reports outside the repository and does not append papers. `--limit` caps retrieved candidates per query, not final accepted additions. Review errors and truncation; reports are not exhaustive literature surveys.

Require formal journal/conference publication or a credible institutional technical report. No ordinary arXiv/bioRxiv preprints are newly accepted; naming a preprint a report is not sufficient. Historical preprint lookup remains available for version verification, not active discovery.

Verify peptide relevance, DOI, authors, title and actual publication date against primary sources. Check DOI, related preprint/journal DOI and normalized title for duplicates. Reference-list DOIs do not establish the identity of the note being reviewed. Keep code/dataset links only when explicitly supplied by the paper, authors or official project.

Classify by the primary contribution, not by the presence of AI. Put reviews in Reviews, benchmark/dataset releases in Data, methods in their technical chapter, and validated application studies in Applications when that is their main contribution. Use exact section/subsection labels from config; use tags for secondary topics.

## Editorial Metadata

- Dates may be `YYYY`, `YYYY-M` or `YYYY-M-D`; never invent month/day or substitute Crossref registration dates. Resolve partial dates against a primary source before accepting a paper into a precise discovery window.
- Note and acceptance dates are not publication evidence. Verified partial dates are sufficient for paper-read ingestion, which has no lower date cutoff.
- Leave optional fields blank when unknown. Write short factual abstract summaries.
- Leave `quality` blank by default; `high` needs demonstrated significance, not merely a prestigious venue.
- Leave `pined` blank by default; `true` selects a paper and `false` does not. Keep pinned papers at or below the configured limit.
- Use a few slash-separated canonical method/domain tags. Resource/person tags are optional. Add genuinely needed vocabulary before using it; review suggestions instead of applying them blindly.

## Metadata And Generation

Ordinary generation prefers the tracked snapshot; missing records can use network APIs. Explicit refresh updates the snapshot, and failures with an existing record produce a visible fallback warning.

```bash
awe-pep --refresh-metadata --as-of 2026-10-03
awe-pep --offline --as-of 2026-10-03
```

`--offline` forbids metadata requests and fails if a snapshot is missing. `--as-of` fixes the recent-paper reference date; future publications are never recent. Partial dates qualify as recent only when their entire possible interval is within the window. Retain `verified_publish_date` with a primary-source URL in a snapshot when an API supplies only a partial date.

## Checks

```bash
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py --strict
python -m unittest discover -s tests -v
python -m build
```

For read-only generation:

```python
from awepep.paper import PaperList
md = PaperList("data/paper.csv", offline=True).get_md(write=False, as_of="2026-10-03")
```

Regenerate only after source/template changes and inspect the README diff for missing papers, resource links and broken anchors. CI checks Python 3.9 and 3.12 offline; there is no scheduled paper-adding workflow. Keep release version and CHANGELOG aligned with substantive changes.

Report paper-read additions, independent supplements, formal-version upgrades, archive moves and unresolved evidence separately, with primary source links. Skill instructions and helpers are tracked with the project and updated through normal repository changes.
