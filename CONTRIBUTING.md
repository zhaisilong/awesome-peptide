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
- `DATABASE.md`: Chapter 0 resource tables and guides, not a second paper list.
- `awepep/config.py`: ordered taxonomy and canonical tag vocabulary.
- `awepep/template.py`: public README wording and formatting.
- `README.md`: generated output, not a paper-editing source.
- `.codex/skills/`: shared on-demand curation and maintenance workflows.

Keep CSV column order unchanged:

```text
title,sec,subsec,authors,publications,code,dataset,quality,publish_date,abstract,blogs,pined,tags
doi,title,source,sec,subsec,code,dataset,quality,pined,tags
```

Use a Markdown DOI link for `publications`. Paper-read rows store a raw DOI and note path/permalink in `source`; do not duplicate generated bibliographic fields there.

## On-Demand Discovery

Update the submodule only when discovering new notes:

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
awe-discover --since 2026-06-16 --until 2026-10-03 --limit 200
```

Choose the requested date window, not the example dates above. The command reads paper-read, Crossref, PubMed and arXiv and writes Markdown/JSON reports outside the repository. It does not append papers. Review provider errors, per-query limits and truncation before describing coverage; a candidate report is not an exhaustive literature survey.

Verify peptide relevance, DOI, authors, title and actual publication date against primary sources. Check DOI, related preprint/journal DOI and normalized title for duplicates. Reference-list DOIs do not establish the identity of the note being reviewed. Keep code/dataset links only when explicitly supplied by the paper, authors or official project.

Classify by the primary contribution, not by the presence of AI. Put reviews in Reviews, benchmark/dataset releases in Data, methods in their technical chapter, and validated application studies in Applications when that is their main contribution. Use exact section/subsection labels from config; use tags for secondary topics.

## Editorial Metadata

- Dates may be `YYYY`, `YYYY-M` or `YYYY-M-D`; never invent month/day or substitute Crossref registration dates. Resolve partial dates against a primary source before accepting a paper into a precise discovery window.
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
