# Agent Guide

Use the repo-local skills in `.codex/skills` for recurring work:

- `$curate-peptide-papers`: add, verify, classify, and validate paper metadata.
- `$maintain-awepep-tooling`: update the Python package, templates, checks, CI, and docs.

## Source Of Truth

- Edit `data/paper.csv` for manually curated paper entries.
- Edit `data/paper-read.csv` for paper-read sourced entries. Keep it minimal and let Crossref or the arXiv fallback fill bibliographic metadata during README generation.
- Use canonical tags from `awepep.config.tag_groups`. Add new tags to the vocabulary before using them, and treat tag audit warnings as curation debt.
- Edit `DATABASE.md` for Chapter 0 content.
- Treat `README.md` as generated output from CSV, `DATABASE.md`, and `awepep/template.py`.
- Do not hand-edit generated paper sections in `README.md` unless the user explicitly asks for a one-off patch.
- Treat `vendor/paper-read` as an external source submodule. Do not edit files inside it; update it with `git submodule update --remote vendor/paper-read`.

## Paper-Read Curation

Use `$curate-peptide-papers` when pulling latest paper notes from `vendor/paper-read`.

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
python .codex/skills/curate-peptide-papers/scripts/scan_paper_read_candidates.py --limit 200 --enrich-crossref
```

Use the scanner report to curate high-confidence peptide/deep-learning papers into `data/paper-read.csv`. The agent must choose `sec/subsec` from the README taxonomy; Crossref and arXiv only supply bibliographic fields. Use GitHub/code links only when the note or primary source explicitly provides them.

## Required Checks

```bash
python -m pip install -e ".[dev]"
git submodule update --init --recursive
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv").get_md(write=False)
print(len(md), md.splitlines()[0])
PY
```

Regenerate `README.md` with `awe-pep` only when CSV or template changes need to be reflected in generated output. This uses Crossref and arXiv when `data/paper-read.csv` contains rows, so network access is required.
