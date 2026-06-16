# Contributing

Thanks for helping improve `awesome-peptide`. This repository is primarily a curated paper list generated from structured CSV metadata.

## Setup

```bash
git clone git@github.com:zhaisilong/awesome-peptide.git
cd awesome-peptide

mamba create -n awepep python=3.9
mamba activate awepep

python -m pip install -e ".[dev]"
```

## Project Layout

- `data/paper.csv`: source of truth for manually curated paper metadata.
- `data/paper-read.csv`: minimal source table for paper-read entries enriched from Crossref during README generation.
- `awepep/template.py`: Liquid templates for generated Markdown.
- `awepep/paper.py`: README generation from CSV data.
- `awepep/check.py`: CSV validation and summary statistics.
- `awepep/config.py`: section order, subsection order, linked tags, and pinned/recent settings.
- `DATABASE.md`: manually maintained Chapter 0 content inserted into `README.md`.
- `resource/`: local paper resources referenced by CSV rows.
- `.codex/skills/`: repo-local Codex skills for paper curation and tooling maintenance.
- `pyproject.toml`: package metadata, dependencies, and console scripts.

## Paper Updates

Edit `data/paper.csv` for manually curated paper metadata changes. Keep the column order unchanged:

```text
title,sec,subsec,authors,publications,code,dataset,quality,publish_date,abstract,blogs,pined,tags
```

Use section and subsection names from `awepep/config.py`. Keep `publications` as a Markdown DOI link so the checker can extract duplicate DOI values.

For papers sourced from `vendor/paper-read`, prefer `data/paper-read.csv` instead of duplicating Crossref metadata. Keep its column order unchanged:

```text
doi,title,source,sec,subsec,code,dataset,quality,pined,tags
```

The README generator fetches authors, publication venue, publish date, DOI link, and abstract from Crossref at generation time. The `sec` and `subsec` values are still agent-curated from the existing awesome-peptide taxonomy.

## Validation

Run the checker before regenerating the README:

```bash
awe-check
```

Run a no-write generation smoke test:

```bash
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv").get_md(write=False)
print(len(md), md.splitlines()[0])
PY
```

Regenerate `README.md` after CSV or template changes:

```bash
awe-pep
git diff -- README.md
```

`awe-pep` uses the Crossref API when `data/paper-read.csv` is present, so README regeneration needs network access.

## Quality And Pinned Papers

- Leave `quality` blank by default; use `high` for landmark or especially relevant work.
- Leave `pined` blank by default; use `true` only for selected important papers.
- Keep abstracts concise when included.
- Use slash-separated tags, for example `Diffusion/Cyclic/MD`.
