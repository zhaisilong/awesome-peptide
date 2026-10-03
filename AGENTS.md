# Agent Guide

Use the repo-local skills in `.codex/skills` for recurring work:

- `$curate-peptide-papers`: add, verify, classify, and validate paper metadata.
- `$maintain-awepep-tooling`: update the Python package, templates, checks, CI, and docs.

## Source Of Truth

- Edit `data/paper.csv` for manually curated paper entries.
- Edit `data/paper-read.csv` for paper-read sourced entries. Keep it minimal; bibliographic metadata is recorded in `data/paper-read-metadata.json` from Crossref or arXiv.
- Keep metadata snapshots tracked with their source and retrieval time. Refresh explicitly; use offline generation for review and CI.
- Use canonical tags from `awepep.config.tag_groups`. Add new tags to the vocabulary before using them, and treat tag audit warnings as curation debt.
- Edit `DATABASE.md` for Chapter 0 resource tables and guides. Store benchmark/dataset papers in CSV, not a second manual paper list.
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

Use the scanner report to curate verified peptide papers into `data/paper-read.csv`; experimental and computational work are both in scope. Choose `sec/subsec` by primary contribution from `awepep.config.sections`; APIs only supply bibliographic fields. Use code/data links only when the note or primary source explicitly associates them with the paper.

## On-Demand Discovery

```bash
awe-discover --since 2026-06-16 --until 2026-10-03 --limit 200
```

Replace the example window with the requested dates. Review Markdown/JSON reports, provider errors and truncation before curating. The command does not modify CSVs. Verify primary identifiers, title duplicates and preprint/journal relationships. Preserve partial publication dates; registration or note dates are not publication evidence. No scheduled paper-adding Actions are needed.

## Required Checks

```bash
python -m pip install -e ".[dev]"
git submodule update --init --recursive
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py --strict
python -m unittest discover -s tests -v
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv", offline=True).get_md(write=False)
print(len(md), md.splitlines()[0])
PY
```

Regenerate only after source/template changes. Use `awe-pep --refresh-metadata` to update snapshots online, then `awe-pep --offline --as-of YYYY-MM-DD` for reproducible output. Missing offline records fail; cached refresh fallback warns. Review generated anchors and content before committing.
